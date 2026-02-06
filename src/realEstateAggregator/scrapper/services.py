import asyncio
import logging
import os
import re
from typing import Generator
from urllib.parse import urljoin

from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from realEstateAggregator.models import Property

from .schemas import PropertySchema

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

logger = logging.getLogger(__name__)

async def run_scraper_async(max_pages=3):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(extra_http_headers=HEADERS)

        urls = [
            urljoin(
                os.getenv('URL_ROOT'), f"vente/{i}"
            ) for i in range(1, max_pages + 1)
        ]

        for url in urls:
            soup = await fetch_page(context, url)
            if not soup:
                break

            for data in parse_listing(soup):
                await save_property_async(data)

        await browser.close()


async def fetch_page(context, url: str) -> BeautifulSoup | None:
    try:
        page = await context.new_page()
        await page.goto(url, timeout=60000)
        
        await page.evaluate("""() => {
            const conf = window.CONF || {};
            if (conf.settings) conf.settings.lang = 'en';

            const container = document.querySelector('.ss-content');
            if (container) {
                container.classList.add('ss-open');
                container.style.display = 'block';
                container.style.opacity = '1';
            }

            const enOption = document.querySelector(
                '.ss-option.lang-switch__option--en:not(.ss-disabled)'
            );
            enOption?.click();
        }""")

        await asyncio.sleep(2)

        await page.wait_for_selector(".property-listing-v2__items", timeout=60000)

        await asyncio.sleep(2)

        html = await page.content()

        if "property-listing" not in html:
            logger.info(f"[EMPTY PAGE] {url}")
            return None

        return BeautifulSoup(html, "html.parser")

    except Exception as e:
        logger.exception(f"[FETCH FAILED] {url}: {e}")
        return None

    finally:
        if page:
            await page.close()


def parse_listing(soup: BeautifulSoup) -> Generator[dict, None, None]:
    properties = soup.select("article.property-listing-v2__container")

    for property in properties:
        try:
            price_raw = safe_text(property.select_one("span.__price-value"))
            url = property.select_one("a.item__title")["href"]

            yield {
                "title": safe_text(property.select_one("span.title__content-2")),
                "address": safe_text(property.select_one("span.title__content-1")),
                "description": safe_text(property.select_one("div.item__text-block")),
                "price": get_price(price_raw),
                "currency": get_currency(price_raw),
                "url": urljoin(
                    os.getenv('URL_ROOT'),
                    url
                ),
                "object_id": get_object_id(url),
                "image_url": safe_image_url(
                    property.select_one("img.decorate__img")["src"]
                )
            }

        except Exception as e:
            logger.exception(f"[PARSE FAILED] {e}")
            continue


def get_price(price_value: str) -> int | None:
    import re
    price_match = re.search(r"[\d\s,.]+", price_value)
    if not price_match:
        return None

    cleaned = price_match.group(0).replace(" ", "").replace(",", "")
    return int(cleaned)


def get_currency(price_value: str) -> str:
    currency_match = re.search(r"[^\d\s,.]+", price_value)
    return currency_match.group(0) if currency_match else None


def get_object_id(url: str) -> str:
    match = re.search(r'/(\d+)-[^/]+/?$', url)
    return int(match.group(1))


async def save_property_async(data) -> None:
    try:
        schema = PropertySchema(**data)
        validated_data = schema.dict()

        await sync_to_async(Property.objects.update_or_create)(
            object_id=validated_data["object_id"],
            defaults=validated_data,
        )

    except Exception:
        logger.exception("Failed to validate or save property")


def safe_text(el):
    return el.get_text(strip=True) if el else None


def safe_image_url(url: str) -> str | None:
    if not url:
        return None

    if url.startswith("//"):
        return "https:" + url

    if url.startswith("/"):
        return urljoin(os.getenv('URL_ROOT'), url)
    return url