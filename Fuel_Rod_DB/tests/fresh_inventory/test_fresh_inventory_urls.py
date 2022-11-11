import pytest
from django.urls import reverse

from fresh_inventory.models import RawRod


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
def test_url_delete(client, user, user_admin, rod_factory):
    """
    Fresh_inventory:create test
    """
    rod = rod_factory(_quantity=2)
    url_1 = reverse('fresh_inventory:delete', args=[rod[0].pk])
    url_2 = reverse('fresh_inventory:delete', args=[rod[1].pk])
    # response for anonymous user
    response_anon = client.get(url_1)
    client.force_login(user=user)
    # response for regular user
    response_user = client.get(url_1)
    client.force_login(user=user_admin)
    # response for admin user
    response_admin = client.get(url_2)
    # only authenticated users are allowed
    assert response_anon.status_code == 302
    assert response_user.status_code == 302
    assert response_admin.status_code == 302
    assert not RawRod.objects.filter(id=rod[0].pk).exists()
    assert not RawRod.objects.filter(id=rod[1].pk).exists()


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
