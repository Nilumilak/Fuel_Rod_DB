import pytest
from django.urls import reverse

from rod_pieces.models import RodPiece


@pytest.mark.django_db
def test_url_table(client, rod_piece_factory):
    rod = rod_piece_factory(material='Cr-PVD-TE01-R01')
    url = reverse('rod_pieces:table', args=[rod.rod_id])
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_url_create(client, user, user_admin, rod_piece_factory):
    rod = rod_piece_factory()
    url = reverse('rod_pieces:create', args=[rod.rod_id])
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
def test_url_delete(client, user, user_admin, rod_piece_factory):
    """
    Fresh_inventory:create test
    """
    rod = rod_piece_factory(_quantity=2)
    url_1 = reverse('rod_pieces:delete', args=[rod[0].pk])
    url_2 = reverse('rod_pieces:delete', args=[rod[1].pk])
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
    assert not RodPiece.objects.filter(id=rod[0].pk).exists()
    assert not RodPiece.objects.filter(id=rod[1].pk).exists()
