import pytest
from django.db import IntegrityError

from rod_pieces.models import SampleState


@pytest.mark.django_db
def test_create_material(sample_state_factory):
    material = sample_state_factory(_quantity=1)

    assert SampleState.objects.filter(id=material[0].pk).exists()


@pytest.mark.django_db
def test_create_materials(sample_state_factory):
    sample_state_factory(_quantity=5)

    assert SampleState.objects.count() == 5


@pytest.mark.django_db
def test_update_material(sample_state_factory):
    material = sample_state_factory(_quantity=1)
    material_db = SampleState.objects.get(id=material[0].pk)
    material_db.name = 'test'
    material_db.save()

    assert SampleState.objects.get(id=material[0].pk).name == 'test'


@pytest.mark.django_db
def test_delete_material(sample_state_factory):
    material = sample_state_factory(_quantity=1)
    SampleState.objects.filter(id=material[0].pk).delete()

    assert not SampleState.objects.filter(id=material[0].pk).exists()


@pytest.mark.django_db
def test_create_materials_name_unique_constraint(sample_state_factory):
    material = sample_state_factory(_quantity=1)

    try:
        SampleState.objects.create(name=material[0].name)
        assert False
    except IntegrityError:
        assert True

