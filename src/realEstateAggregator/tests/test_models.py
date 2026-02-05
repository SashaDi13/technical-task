import pytest
from django.core.exceptions import ValidationError
from realEstateAggregator.models import Property


@pytest.mark.django_db
def test_extract_object_id_valid_url():
    url = "https://example.com/vente/1234-some-property/"
    property = Property(
        title="Test",
        price=100000,
        url=url,
        address="Test Address",
        object_id=0
    )
    object_id = property.extract_object_id()
    assert object_id == 1234


@pytest.mark.django_db
def test_extract_object_id_invalid_url():
    url = "https://example.com/vente/no-id-here/"
    property = Property(
        title="Test",
        price=100000,
        url=url,
        address="Test Address",
        object_id=0
    )
    with pytest.raises(ValidationError):
        property.extract_object_id()


@pytest.mark.django_db
def test_clean_sets_object_id():
    url = "https://example.com/vente/5678-some-property/"
    property = Property(
        title="Test",
        price=100000,
        url=url,
        address="Test Address",
        object_id=None
    )
    property.clean()
    assert property.object_id == 5678


@pytest.mark.django_db
def test_save_fails_without_object_id():
    url = "https://example.com/vente/9012-another-property/"
    property = Property(
        title="Test Save",
        price=50000,
        url=url,
        address="Test Address",
        object_id=None
    )

    with pytest.raises(ValidationError):
        property.save()


@pytest.mark.django_db
def test_unique_object_id_constraint():
    Property.objects.create(
        title="Property1",
        price=100,
        url="https://example.com/vente/1111-property/",
        address="A",
        object_id=1111
    )

    prop2 = Property(
        title="Property2",
        price=200,
        url="https://example.com/vente/1111-another-property/",
        address="B",
        object_id=1111
    )

    with pytest.raises(ValidationError):
        prop2.save()

