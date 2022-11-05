import pytest

from dry_storage.models import RodDryStorageTest
from fresh_inventory.models import RawRod


@pytest.mark.django_db
def test_create_test(dry_storage_test_factory):
    rod = dry_storage_test_factory(_quantity=1)
    rod_db = RodDryStorageTest.objects.get(id=rod[0].pk)

    assert RodDryStorageTest.objects.filter(id=rod[0].pk).exists()
    assert rod_db.number == RodDryStorageTest.objects.filter(raw_rod=rod_db.raw_rod).count()
    assert rod_db.rod_id == f'{rod_db.raw_rod.exp_id}-R{rod_db.number:02}'


@pytest.mark.django_db
def test_create_tests(dry_storage_test_factory):
    dry_storage_test_factory(_quantity=5)

    assert RodDryStorageTest.objects.count() == 5
    assert list(RodDryStorageTest.objects.all()) == list(RodDryStorageTest.objects.all().order_by('rod_id'))


@pytest.mark.django_db
def test_create_test_with_same_fresh_material(dry_storage_test_factory, dry_storage_exp_factory):
    raw_rod = dry_storage_exp_factory(_quantity=1)[0]
    rods = dry_storage_test_factory(_quantity=2, raw_rod=raw_rod)

    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_update_test(dry_storage_test_factory, dry_storage_exp_factory):
    raw_rod = dry_storage_exp_factory(_quantity=1)[0]
    rod = dry_storage_test_factory(_quantity=5, raw_rod=raw_rod)
    rod_db = RodDryStorageTest.objects.get(id=rod[0].pk)
    rod_db.original_length = 1
    rod_db.save()
    assert RodDryStorageTest.objects.get(id=rod[0].pk).original_length == 1
    assert RodDryStorageTest.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_test(dry_storage_test_factory):
    rod = dry_storage_test_factory()
    length = rod.raw_rod.material.length
    RodDryStorageTest.objects.filter(id=rod.pk).delete()
    assert not RodDryStorageTest.objects.filter(id=rod.pk).exists()
    assert RawRod.objects.get(id=rod.raw_rod.material.pk).length == length + rod.original_length


@pytest.mark.django_db
def test_delete_test_with_material(dry_storage_test_factory, dry_storage_exp_factory, rod_factory, material_factory):
    material = material_factory(_quantity=1)[0]
    fresh_rod = rod_factory(_quantity=1, material=material)[0]
    raw_rod = dry_storage_exp_factory(_quantity=1, material=fresh_rod)[0]
    rod = dry_storage_test_factory(_quantity=1, raw_rod=raw_rod)
    material.delete()
    assert not RodDryStorageTest.objects.filter(id=rod[0].pk).exists()