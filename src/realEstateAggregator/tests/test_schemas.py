import pytest
from pydantic import ValidationError

from realEstateAggregator.scrapper.schemas import PropertySchema


def test_property_schema_valid():
    data = {
        "title": "Nice apartment",
        "price": 100000,
        "description": "Great place",
        "address": "Paris",
        "object_id": 1234,
        "url": "https://example.com/vente/1234-apartment/",
        "image_url": "https://example.com/images/1.jpg",
    }

    schema = PropertySchema(**data)

    assert schema.object_id == 1234
    assert str(schema.url).startswith("https://")


def test_property_schema_invalid_url():
    data = {
        "title": "Nice apartment",
        "price": 100000,
        "description": "Great place",
        "address": "Paris",
        "object_id": 1234,
        "url": "not-a-url",
        "image_url": "https://example.com/images/1.jpg",
    }

    with pytest.raises(ValidationError):
        PropertySchema(**data)


def test_property_schema_missing_field():
    data = {
        "title": "Nice apartment",
        "price": 100000,
        "description": "Great place",
        "address": "Paris",
        "url": "https://example.com/vente/1234-apartment/",
        "image_url": "https://example.com/images/1.jpg",
    }

    with pytest.raises(ValidationError):
        PropertySchema(**data)
