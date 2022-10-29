import pytest
from django.urls import reverse


# @pytest.mark.django_db
# def test_url_table(client, dry_storage_test_factory):
#     url = reverse('dry_storage:table')
#     response = client.get(url)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_url_create(client, user, user_admin):
#     url = reverse('dry_storage:create')
#     response_anon = client.get(url)
#     client.force_login(user=user)
#     response_user = client.get(url)
#     client.force_login(user=user_admin)
#     response_admin = client.get(url)
#     assert response_anon.status_code == 302
#     assert response_user.status_code == 200
#     assert response_admin.status_code == 200