import pytest
from django.urls import reverse

from dry_storage_exp.models import DryStorageExp


@pytest.mark.django_db
def test_url_table(client, dry_storage_test_factory):
    """
    Dry_storage_exp:table test
    """
    url = reverse('dry_storage_exp:table')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_url_create(client, user, user_admin):
    """
    Dry_storage_exp:create test
    """
    url = reverse('dry_storage_exp:create')
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
def test_url_delete(client, user, user_admin, dry_storage_exp_factory):
    """
    Fresh_inventory:create test
    """
    rod = dry_storage_exp_factory(_quantity=2)
    url_1 = reverse('dry_storage_exp:delete', args=[rod[0].pk])
    url_2 = reverse('dry_storage_exp:delete', args=[rod[1].pk])
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
    assert not DryStorageExp.objects.filter(id=rod[0].pk).exists()
    assert not DryStorageExp.objects.filter(id=rod[1].pk).exists()
