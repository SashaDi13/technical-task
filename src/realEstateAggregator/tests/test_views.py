import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from realEstateAggregator.models import Property
from unittest.mock import patch

@pytest.mark.django_db
def test_home_view(client):
    property = Property.objects.create(
        title="Property1", price=100, url="https://example.com/vente/1-test/", address="Addr1", object_id=1
    )
    url = reverse('home')
    response = client.get(url)

    assert response.status_code == 200
    assert 'home.html' in [t.name for t in response.templates]
    assert property.title in response.content.decode()

@pytest.mark.django_db
@patch('realEstateAggregator.views.run_scraper_task_async.delay')
def test_run_scraper_view_post(mock_delay, client):
    url = reverse('run_scraper')
    response = client.post(url)

    mock_delay.assert_called_once()
    assert response.status_code == 302
    assert response.url == reverse('home')

@pytest.mark.django_db
def test_add_property_view_get(client):
    url = reverse('add_property')
    response = client.get(url)

    assert response.status_code == 200
    assert 'Add Property' in response.content.decode()
    assert 'form' in response.context


@pytest.mark.django_db
def test_add_property_view_post_success(client, settings):
    settings.URL_ROOT = "https://example.com/"

    url = reverse('add_property')
    data = {
        "title": "New Property",
        "price": 1234,
        "url": "https://example.com/vente/2-test/",
        "address": "Addr",
        "currency": "USD",
        "description": "Desc",
        "image_url": "https://example.com/1.jpg",
    }

    response = client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("home")
    assert Property.objects.filter(title="New Property").exists()

@pytest.mark.django_db
def test_add_property_view_post_invalid(client):
    url = reverse('add_property')
    data = {"title": ""}
    response = client.post(url, data)

    assert response.status_code == 200
    assert 'Add Property' in response.content.decode()
    assert 'form' in response.context
    assert response.context['form'].errors


@pytest.mark.django_db
def test_update_property_view_get(client):
    property = Property.objects.create(
        title="PropertyToUpdate", price=100, url="https://example.com/vente/3-test/", address="Addr3", object_id=3
    )
    url = reverse('update_property', kwargs={'id': property.id})
    response = client.get(url)

    assert response.status_code == 200
    assert 'Update Property' in response.content.decode()
    assert response.context['form'].instance == property


@pytest.mark.django_db
def test_update_property_view_post_success(client):
    property = Property.objects.create(
        title="OldTitle", price=100, url="https://example.com/vente/4-test/", address="Addr4", object_id=4
    )
    url = reverse('update_property', kwargs={'id': property.id})
    data = {
        "title": "UpdatedTitle",
        "price": 200,
        "address": "AddrUpdated",
        "currency": "USD",
        "description": "UpdatedDesc",
        "image_url": "https://example.com/2.jpg"
    }
    response = client.post(url, data)

    property.refresh_from_db()
    messages = list(get_messages(response.wsgi_request))

    assert property.title == "UpdatedTitle"
    assert any("Property updated successfully" in str(m) for m in messages)
    assert response.status_code == 302
    assert response.url == reverse('home')


@pytest.mark.django_db
def test_delete_property_view_get(client):
    property = Property.objects.create(
        title="ToDelete",
        price=100,
        url="https://example.com/vente/5-test/",
        address="Addr5",
        object_id=5
    )
    assert property.id, "Property не має id!"
    url = reverse('delete_property', kwargs={'id': property.id})
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_property_view_post(client):
    property = Property.objects.create(
        title="ToDelete", price=100, url="https://example.com/vente/6-test/", address="Addr6", object_id=6
    )
    url = reverse('delete_property', kwargs={'id': property.id})
    response = client.post(url)

    messages = list(get_messages(response.wsgi_request))
    assert not Property.objects.filter(id=property.id).exists()
    assert any("Property deleted successfully" in str(m) for m in messages)
    assert response.status_code == 302
    assert response.url == reverse('home')
