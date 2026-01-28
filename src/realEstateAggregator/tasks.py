from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from .models import Property


def real_estate_scraper():
    url_root = "https://www.lemasson-conseil.com/"
    url = url_root + "vente/"

    get_property(url_root, url)


def get_property(url_root, url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    properties = soup.find_all("article", {"class": "property-listing-v2__container"})

    for property in properties:
        title = property.find("span", {"class": "title__content-2"}).text
        address = property.find("span", {"class": "title__content-1"}).text
        description = property.find("div", {"class": "item__text-block"}).text
        price = property.find("span", {"class": "__price-value"}).text
        href = property.find("a", {"class": "item__title"})["href"]
        url = urljoin(url_root, href)
        image_url = property.find("img", {"class": "decorate__img"})["src"]

        Property.objects.update_or_create(
            url=url,
            defaults={
                "title": title,
                "price": price,
                "description": description,
                "address": address,
                "image_url": image_url
            }
        )

    url_tag = soup.find_all("a", {"class": "pagination__link"})[-1]
    if url_tag and url_tag.get("href") and '3' not in url_tag.get("href"):
        url = url_root + url_tag.get("href")
        get_property(url_root, url)