import pytest
from model_bakery import baker


# Client, User
from django.contrib.auth.models import User
from rest_framework.test import APIClient


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


# fresh_inventory fixtures
from fresh_inventory.models import Material, RawRod, RawRodNote


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


# dry_storage_exp fixtures
from dry_storage_exp.models import DryStorageExp, DryStorageExpNote


@pytest.fixture
def dry_storage_exp_factory():
    def factory(*args, **kwargs):
        return baker.make(DryStorageExp, *args, **kwargs)

    return factory


@pytest.fixture
def dry_storage_exp_note_factory():
    def factory(*args, **kwargs):
        return baker.make(DryStorageExpNote, *args, **kwargs)

    return factory


# dry_storage fixtures
from dry_storage.models import RodDryStorageTest, RodDryStorageTestNote


@pytest.fixture
def dry_storage_test_factory():
    def factory(*args, **kwargs):
        return baker.make(RodDryStorageTest, *args, **kwargs)

    return factory


@pytest.fixture
def dry_storage_test_note_factory():
    def factory(*args, **kwargs):
        return baker.make(RodDryStorageTestNote, *args, **kwargs)

    return factory
