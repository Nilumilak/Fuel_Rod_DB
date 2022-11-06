import pytest
from django.db import IntegrityError

from rod_pieces.models import SampleState


@pytest.mark.django_db
def test_create_sample_state(sample_state_factory):
    """
    Create one SampleState
    """
    material = sample_state_factory()

    assert SampleState.objects.filter(id=material.pk).exists()


@pytest.mark.django_db
def test_create_sample_states(sample_state_factory):
    """
    Create many SampleState
    """
    sample_state_factory(_quantity=5)

    assert SampleState.objects.count() == 5


@pytest.mark.django_db
def test_update_sample_state(sample_state_factory):
    """
    Update SampleState
    """
    material = sample_state_factory()
    material_db = SampleState.objects.get(id=material.pk)
    material_db.name = 'test'
    material_db.save()

    assert SampleState.objects.get(id=material.pk).name == 'test'


@pytest.mark.django_db
def test_delete_sample_state(sample_state_factory):
    """
    Delete SampleState
    """
    material = sample_state_factory()
    SampleState.objects.filter(id=material.pk).delete()

    assert not SampleState.objects.filter(id=material.pk).exists()


@pytest.mark.django_db
def test_create_sample_states_name_unique_constraint(sample_state_factory):
    """
    SampleState name should be unique
    """
    material = sample_state_factory()

    try:
        SampleState.objects.create(name=material.name)
        assert False
    except IntegrityError:
        assert True

