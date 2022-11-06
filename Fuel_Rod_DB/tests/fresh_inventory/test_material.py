import pytest
from django.db import IntegrityError

from fresh_inventory.models import Material


@pytest.mark.django_db
def test_create_material(material_factory):
    """
    Create one Material
    """
    material = material_factory()

    assert Material.objects.filter(id=material.pk).exists()


@pytest.mark.django_db
def test_create_materials(material_factory):
    """
    Create many Material
    """
    material_factory(_quantity=5)

    assert Material.objects.count() == 5


@pytest.mark.django_db
def test_update_material(material_factory):
    """
    Update Material
    """
    material = material_factory()
    material_db = Material.objects.get(id=material.pk)
    material_db.name = 'test'
    material_db.save()

    assert Material.objects.get(id=material.pk).name == 'test'


@pytest.mark.django_db
def test_delete_material(material_factory):
    """
    Delete Material
    """
    material = material_factory()
    Material.objects.filter(id=material.pk).delete()

    assert not Material.objects.filter(id=material.pk).exists()


@pytest.mark.django_db
def test_create_materials_name_unique_constraint(material_factory):
    """
    Material name should be unique
    """
    material = material_factory()

    try:
        Material.objects.create(name=material.name)
        assert False
    except IntegrityError:
        assert True

