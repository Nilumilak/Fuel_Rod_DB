import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_url_table(client):
    url = reverse('fresh_inventory:table')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_url_create(client, user, user_admin):
    url = reverse('fresh_inventory:create')
    response_anon = client.get(url)
    client.force_login(user=user)
    response_user = client.get(url)
    client.force_login(user=user_admin)
    response_admin = client.get(url)
    assert response_anon.status_code == 302
    assert response_user.status_code == 200
    assert response_admin.status_code == 200


@pytest.mark.django_db
def test_url_login(client, user):
    url = reverse('fresh_inventory:login')
    response_anon = client.get(url)
    client.force_login(user=user)
    response_user = client.get(url)

    assert response_anon.status_code == 200
    assert response_user.status_code == 200


@pytest.mark.django_db
def test_url_register(client, user):
    url = reverse('fresh_inventory:register')
    response_anon = client.get(url)
    client.force_login(user=user)
    response_user = client.get(url)

    assert response_anon.status_code == 200
    assert response_user.status_code == 200


@pytest.mark.django_db
def test_url_register(client, user):
    url = reverse('fresh_inventory:logout')
    response_anon = client.get(url)
    client.force_login(user=user)
    response_user = client.get(url)

    assert response_anon.status_code == 302
    assert response_user.status_code == 302
