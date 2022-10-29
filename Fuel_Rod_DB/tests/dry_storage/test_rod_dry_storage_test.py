import pytest

from dry_storage.models import RodDryStorageTest


@pytest.mark.django_db
def test_create_test(dry_storage_test_factory):
    rod = dry_storage_test_factory(_quantity=1)
    rod_db = RodDryStorageTest.objects.get(id=rod[0].pk)

    assert RodDryStorageTest.objects.filter(id=rod[0].pk).exists()
    assert rod_db.number == RodDryStorageTest.objects.filter(exp_id=rod_db.exp_id).count()
    assert rod_db.rod_id == f'{rod_db.exp_id}-R{rod_db.number:02}'


@pytest.mark.django_db
def test_create_tests(dry_storage_test_factory):
    dry_storage_test_factory(_quantity=5)

    assert RodDryStorageTest.objects.count() == 5
    assert list(RodDryStorageTest.objects.all()) == list(RodDryStorageTest.objects.all().order_by('rod_id'))


@pytest.mark.django_db
def test_create_test_with_same_fresh_material(dry_storage_test_factory):
    fresh_material = 'test_material'
    rods = dry_storage_test_factory(_quantity=2, exp_id=fresh_material)

    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_update_test(dry_storage_test_factory):
    fresh_material = 'test_material'
    rod = dry_storage_test_factory(_quantity=5, exp_id=fresh_material)
    rod_db = RodDryStorageTest.objects.get(id=rod[0].pk)
    rod_db.original_length = 1
    rod_db.save()
    assert RodDryStorageTest.objects.get(id=rod[0].pk).original_length == 1
    assert RodDryStorageTest.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_test(dry_storage_test_factory):
    rod = dry_storage_test_factory(_quantity=1)
    RodDryStorageTest.objects.filter(id=rod[0].pk).delete()
    assert not RodDryStorageTest.objects.filter(id=rod[0].pk).exists()
