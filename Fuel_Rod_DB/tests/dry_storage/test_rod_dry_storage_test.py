import pytest

from dry_storage.models import RodDryStorageTest
from fresh_inventory.models import RawRod


@pytest.mark.django_db
def test_create_test(dry_storage_test_factory):
    """
    Create one RodDryStorageTest
    """
    rod = dry_storage_test_factory()
    rod_db = RodDryStorageTest.objects.get(id=rod.pk)

    assert RodDryStorageTest.objects.filter(id=rod.pk).exists()
    assert rod_db.number == RodDryStorageTest.objects.filter(raw_rod=rod_db.raw_rod).count()
    assert rod_db.rod_id == f'{rod_db.raw_rod.exp_id}-R{rod_db.number:02}'


@pytest.mark.django_db
def test_create_tests(dry_storage_test_factory):
    """
    Create many RodDryStorageTest
    """
    dry_storage_test_factory(_quantity=5)

    assert RodDryStorageTest.objects.count() == 5
    assert list(RodDryStorageTest.objects.all()) == list(RodDryStorageTest.objects.all().order_by('rod_id'))


@pytest.mark.django_db
def test_number_incrementing(dry_storage_test_factory, dry_storage_exp_factory):
    """
    Numbers should always increase by 1.
    For example: number 6 should be created even if from 5 rods the 3rd was deleted
    """
    raw_rod = dry_storage_exp_factory()
    rods = dry_storage_test_factory(_quantity=5, raw_rod=raw_rod)
    rods[2].delete()
    new_rod = dry_storage_test_factory(raw_rod=raw_rod)
    assert new_rod.number == 6


@pytest.mark.django_db
def test_create_test_with_same_fresh_material(dry_storage_test_factory, dry_storage_exp_factory):
    """
    Create many RodDryStorageTest with the same raw_rod
    """
    raw_rod = dry_storage_exp_factory()
    rods = dry_storage_test_factory(_quantity=2, raw_rod=raw_rod)

    # 'number' is auto-incrementing for rods with the same raw_rod
    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_update_test(dry_storage_test_factory, dry_storage_exp_factory):
    """
    Update RodDryStorageTest
    """
    raw_rod = dry_storage_exp_factory()
    rod = dry_storage_test_factory(_quantity=5, raw_rod=raw_rod)
    rod_db = RodDryStorageTest.objects.get(id=rod[0].pk)
    rod_db.original_length = 1
    rod_db.save()
    assert RodDryStorageTest.objects.get(id=rod[0].pk).original_length == 1
    # 'number' should not change when updating
    assert RodDryStorageTest.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_test(dry_storage_test_factory):
    """
    Delete RodDryStorageTest
    """
    rod = dry_storage_test_factory()
    length = rod.raw_rod.material.length
    RodDryStorageTest.objects.filter(id=rod.pk).delete()
    assert not RodDryStorageTest.objects.filter(id=rod.pk).exists()
    # the length of particular RawRod should automatically increase
    assert RawRod.objects.get(id=rod.raw_rod.material.pk).length == length + (rod.original_length or 0)


@pytest.mark.django_db
def test_delete_test_with_material(dry_storage_test_factory, dry_storage_exp_factory, rod_factory, material_factory):
    """
    RodDryStorageTest should automatically delete with its material
    """
    material = material_factory()
    fresh_rod = rod_factory(material=material)
    raw_rod = dry_storage_exp_factory(material=fresh_rod)
    rod = dry_storage_test_factory(raw_rod=raw_rod)
    material.delete()
    assert not RodDryStorageTest.objects.filter(id=rod.pk).exists()


@pytest.mark.django_db
def test_subtract_length_from_original_raw(rod_factory, dry_storage_test_factory):
    """
    Length of particular RawRod decreases when creates new RodDryStorageTest
    """
    raw_rod = rod_factory()
    previous_length = raw_rod.length

    dry_storage_test_factory(raw_rod__material=raw_rod, original_length=1000)

    assert previous_length == raw_rod.length + 1000


@pytest.mark.django_db
def test_change_length_of_original_raw(rod_factory, dry_storage_test_factory):
    """
    Length of particular RawRod changes when updates new RodDryStorageTest
    """
    raw_rod = rod_factory()
    previous_raw_rod_length = raw_rod.length

    rod = dry_storage_test_factory(raw_rod__material=raw_rod, original_length=2000)
    previous_dry_storage_length = rod.original_length
    rod.original_length = 1000
    rod.save()

    assert raw_rod.length == previous_raw_rod_length - previous_dry_storage_length + rod.original_length
