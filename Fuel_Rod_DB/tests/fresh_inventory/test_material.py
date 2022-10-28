import pytest
from django.db import IntegrityError

from fresh_inventory.models import Material


@pytest.mark.django_db
def test_create_material(material_factory):
    material = material_factory(_quantity=1)

    assert Material.objects.filter(id=material[0].pk).exists()


@pytest.mark.django_db
def test_create_materials(material_factory):
    material_factory(_quantity=5)

    assert Material.objects.count() == 5


@pytest.mark.django_db
def test_update_material(material_factory):
    material = material_factory(_quantity=1)
    material_db = Material.objects.get(id=material[0].pk)
    material_db.name = 'test'
    material_db.save()

    assert Material.objects.get(id=material[0].pk).name == 'test'


@pytest.mark.django_db
def test_delete_material(material_factory):
    material = material_factory(_quantity=1)
    Material.objects.filter(id=material[0].pk).delete()

    assert not Material.objects.filter(id=material[0].pk).exists()


@pytest.mark.django_db
def test_create_materials_name_unique_constraint(material_factory):
    material = material_factory(_quantity=1)

    try:
        Material.objects.create(name=material[0].name)
        assert False
    except IntegrityError:
        assert True

