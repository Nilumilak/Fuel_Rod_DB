import pytest

from fresh_inventory.models import RawRod, Material


@pytest.mark.django_db
def test_create_rod(rod_factory):
    """
    Create one RawRod
    """
    rod = rod_factory()
    rod_db = RawRod.objects.get(id=rod.pk)

    assert RawRod.objects.filter(id=rod.pk).exists()
    assert rod_db.number == RawRod.objects.filter(material=rod_db.material).count()
    assert rod_db.rod_id == f'{rod_db.material}-{rod_db.number:02}'


@pytest.mark.django_db
def test_create_rods(rod_factory):
    """
    Create many RawRod
    """
    rod_factory(_quantity=5)

    assert RawRod.objects.count() == 5
    assert list(RawRod.objects.all()) == list(RawRod.objects.all().order_by('rod_id'))


@pytest.mark.django_db
def test_create_rods_with_same_material(rod_factory, material_factory):
    """
    Create RawRod with the same material
    """
    material = material_factory()
    rods = rod_factory(_quantity=2, material=material)

    # 'number' is auto-incrementing for rods with the same material
    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_update_rod(rod_factory, material_factory):
    """
    Update RawRod
    """
    material = material_factory()
    rod = rod_factory(_quantity=5, material=material)
    rod_db = RawRod.objects.get(id=rod[0].pk)
    rod_db.length = 1
    rod_db.save()
    assert RawRod.objects.get(id=rod[0].pk).length == 1
    # 'number' should not change when updating
    assert RawRod.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_rod(rod_factory):
    """
    Delete RawRod
    """
    rod = rod_factory()
    RawRod.objects.filter(id=rod.pk).delete()
    assert not RawRod.objects.filter(id=rod.pk).exists()


@pytest.mark.django_db
def test_delete_rod_with_material(rod_factory):
    """
    RawRod should automatically delete with its material
    """
    rod = rod_factory()
    Material.objects.get(id=rod.material.pk).delete()
    assert not RawRod.objects.all().exists()
