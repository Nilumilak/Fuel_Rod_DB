import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker

from fresh_inventory.models import Material, RawRod, RawRodNote


@pytest.fixture
@pytest.mark.django_db
def user():
    return User.objects.create_user(
        username='user',
        password='user',
        is_staff=False,
    )


@pytest.fixture
@pytest.mark.django_db
def user_admin():
    return User.objects.create_user(
        username='admin',
        password='admin',
        is_staff=True,
    )


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def material_factory():
    def factory(*args, **kwargs):
        return baker.make(Material, *args, **kwargs)

    return factory


@pytest.fixture
def rod_factory():
    def factory(*args, **kwargs):
        return baker.make(RawRod, *args, **kwargs)

    return factory


@pytest.fixture
def note_factory():
    def factory(*args, **kwargs):
        return baker.make(RawRodNote, *args, **kwargs)

    return factory


# @pytest.fixture
# def create_note(rod_factory, note_factory, material_factory)