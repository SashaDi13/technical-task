from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup

from realEstateAggregator.scrapper.services import (
    get_currency,
    get_object_id,
    get_price,
    parse_listing,
    safe_image_url,
    save_property_async,
)

HTML = """
<article class="property-listing-v2__container">
  <span class="__price-value">123 000 €</span>
  <a class="item__title" href="/vente/1234-nice-house/"></a>
  <span class="title__content-2">Nice house</span>
  <span class="title__content-1">Paris</span>
  <div class="item__text-block">Great property</div>
  <img class="decorate__img" src="/img/1.jpg"/>
</article>
"""


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("123 000 €", 123000),
        ("99,500 USD", 99500),
        ("100000", 100000),
    ],
)


def test_get_price(raw, expected):
    assert get_price(raw) == expected


def test_get_currency():
    assert get_currency("123 000 €") == "€"
    assert get_currency("99,500 USD") == "USD"


def test_get_object_id():
    url = "/vente/1234-some-property/"
    assert get_object_id(url) == 1234


def test_safe_image_url_relative(monkeypatch):
    monkeypatch.setenv("URL_ROOT", "https://example.com/")
    assert safe_image_url("/img/test.jpg") == "https://example.com/img/test.jpg"


def test_safe_image_url_protocol_relative():
    assert safe_image_url("//cdn.test.com/a.jpg") == "https://cdn.test.com/a.jpg"


def test_parse_listing(monkeypatch):
    monkeypatch.setenv("URL_ROOT", "https://example.com/")

    soup = BeautifulSoup(HTML, "html.parser")
    results = list(parse_listing(soup))

    assert len(results) == 1

    item = results[0]
    assert item["title"] == "Nice house"
    assert item["address"] == "Paris"
    assert item["price"] == 123000
    assert item["currency"] == "€"
    assert item["object_id"] == 1234
    assert item["url"] == "https://example.com/vente/1234-nice-house/"


@pytest.mark.asyncio
@patch("realEstateAggregator.scrapper.services.Property.objects.update_or_create")
async def test_save_property_async(mock_update):
    data = {
        "title": "Test",
        "price": 100000,
        "description": "Desc",
        "address": "Paris",
        "object_id": 1234,
        "url": "https://example.com/vente/1234-test/",
        "image_url": "https://example.com/1.jpg",
        "currency": "€",
    }

    await save_property_async(data)

    mock_update.assert_called_once()
