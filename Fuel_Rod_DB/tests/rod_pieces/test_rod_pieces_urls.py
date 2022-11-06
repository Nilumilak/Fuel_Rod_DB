import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_url_table(client, rod_piece_factory):
    rod = rod_piece_factory()
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
