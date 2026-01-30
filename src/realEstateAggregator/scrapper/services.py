import asyncio
from typing import Generator
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from .models import Property
from .schemas import PropertySchema

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

URL_ROOT = "https://www.lemasson-conseil.com/"

async def run_scraper_async(max_pages=3):
    urls = [urljoin(URL_ROOT, f"vente/page-{i}/") for i in range(1, max_pages + 1)]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_page(session, url) for url in urls]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for page in results:
            if isinstance(page, Exception) or page is None:
                continue
            for data in parse_listing(page):
                save_property(data)


async def fetch_page(session: aiohttp.ClientSession, url: str) -> BeautifulSoup:
    try:
        async with session.get(url, headers=HEADERS, timeout=10) as response:
            response.raise_for_status()
            text = await response.text()
            return BeautifulSoup(text, "html.parser")
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def parse_listing(soup: BeautifulSoup) -> Generator[dict, None, None]:
    properties = soup.find_all("article", {"class": "property-listing-v2_container"})

    for property in properties:
        try:
            yield {
                "title": property.find("span", {"class": "title__content-2"})
                            .get_text(strip=True),
                "address": property.find("span", {"class": "title__content-1"})
                            .get_text(strip=True),
                "description": property.find("div", {"class": "item__text-block"})
                            .get_text(strip=True),
                "price": property.find("span", {"class": "__price-value"})
                            .get_text(strip=True),
                "url": urljoin(
                    URL_ROOT, 
                    property.find("a", {"class": "item__title"})["href"]
                ),
                "image_url": property.find("img", {"class": "decorate__img"})["src"]
            }
        except Exception as e:
            print(f"Failed to parse property: {e}")
            continue


def save_property(data: dict) -> None:
    try:
        validated_data = PropertySchema(**data)
        Property.objects.update_or_create(
            url=data["url"],
            defaults=validated_data.dict()
        )
    except Exception as e:
        print(f"Failed to validate or save property: {e}")


def get_next_page(soup: BeautifulSoup) -> str | None:
    btn_next = soup.find_all("a", {"class": "pagination__link"})[-1]

    if btn_next and btn_next["href"]:
        return urljoin(URL_ROOT, btn_next["href"])

    return None