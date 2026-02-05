import os
import pytest
from realEstateAggregator.forms import PropertyCreateForm, PropertyUpdateForm
from realEstateAggregator.models import Property

@pytest.fixture
def valid_data(monkeypatch):
    monkeypatch.setenv("URL_ROOT", "https://example.com/")

    return {
        "title": "Test property",
        "price": 100000,
        "url": "https://example.com/vente/1234-test-property/",
        "currency": "USD",
        "address": "Test address",
        "description": "Desc",
        "image_url": "",
    }


@pytest.mark.django_db
def test_property_create_form_valid(valid_data):
    form = PropertyCreateForm(data=valid_data)

    assert form.is_valid()


@pytest.mark.django_db
def test_property_create_form_requires_url(valid_data):
    valid_data["url"] = ""

    form = PropertyCreateForm(data=valid_data)

    assert not form.is_valid()
    assert "url" in form.errors


@pytest.mark.django_db
def test_property_create_form_invalid_object_id(valid_data):
    valid_data["url"] = "https://example.com/vente/no-id-here/"

    form = PropertyCreateForm(data=valid_data)

    assert not form.is_valid()
    assert "URL має містити правильний формат" in form.errors["url"][0]


@pytest.mark.django_db
def test_property_create_form_sets_object_id(valid_data):
    form = PropertyCreateForm(data=valid_data)

    assert form.is_valid()
    instance = form.save()

    assert instance.object_id == 1234


@pytest.mark.django_db
def test_property_update_form_valid():
    property = Property.objects.create(
        title="Old",
        price=100,
        url="https://example.com/1/",
        address="Addr",
        object_id=1,
    )

    valid_data = {
        "title": "Updated",
        "price": 200,
        "currency": "USD",
        "address": "Test address",
        "description": "Desc",
        "image_url": "https://example.com/1.jpg",
    }

    form = PropertyUpdateForm(data=valid_data, instance=property)

    assert form.is_valid(), form.errors

