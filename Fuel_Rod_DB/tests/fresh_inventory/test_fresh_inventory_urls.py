import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_url_table(client):
    """
    Fresh_inventory:table test
    """
    url = reverse('fresh_inventory:table')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_url_create(client, user, user_admin):
    """
    Fresh_inventory:create test
    """
    url = reverse('fresh_inventory:create')
    # response for anonymous user
    response_anon = client.get(url)
    client.force_login(user=user)
    # response for regular user
    response_user = client.get(url)
    client.force_login(user=user_admin)
    # response for admin user
    response_admin = client.get(url)
    # only authenticated users are allowed
    assert response_anon.status_code == 302
    assert response_user.status_code == 200
    assert response_admin.status_code == 200


@pytest.mark.django_db
def test_url_login(client, user):
    """
    Fresh_inventory:login test
    """
    url = reverse('fresh_inventory:login')
    response_anon = client.get(url)
    client.force_login(user=user)
    response_user = client.get(url)

    assert response_anon.status_code == 200
    assert response_user.status_code == 200


@pytest.mark.django_db
def test_url_register(client, user):
    """
    Fresh_inventory:register test
    """
    url = reverse('fresh_inventory:register')
    response_anon = client.get(url)
    client.force_login(user=user)
    response_user = client.get(url)

    assert response_anon.status_code == 200
    assert response_user.status_code == 200


@pytest.mark.django_db
def test_url_register(client, user):
    """
    Fresh_inventory:logout test
    """
    url = reverse('fresh_inventory:logout')
    response_anon = client.get(url)
    client.force_login(user=user)
    response_user = client.get(url)

    assert response_anon.status_code == 302
    assert response_user.status_code == 302
