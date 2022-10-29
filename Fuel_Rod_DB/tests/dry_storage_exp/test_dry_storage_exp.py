import pytest

from dry_storage_exp.models import DryStorageExp


@pytest.mark.django_db
def test_create_exp(dry_storage_exp_factory):
    rod = dry_storage_exp_factory(_quantity=1)[0]
    rod_db = DryStorageExp.objects.get(id=rod.pk)

    assert DryStorageExp.objects.filter(id=rod.pk).exists()
    assert rod_db.number == DryStorageExp.objects.filter(material__material=rod.material.material).count()
    assert rod_db.exp_id == f'{rod.material.material}-DS{rod.number:02}'


@pytest.mark.django_db
def test_create_exp(dry_storage_exp_factory):
    dry_storage_exp_factory(_quantity=5)

    assert DryStorageExp.objects.count() == 5
    assert list(DryStorageExp.objects.all()) == list(DryStorageExp.objects.all().order_by('exp_id'))


@pytest.mark.django_db
def test_create_exp_with_same_fresh_material(rod_factory, dry_storage_exp_factory):
    material = rod_factory(_quantity=1)[0]
    rods = dry_storage_exp_factory(_quantity=2, material=material)

    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_update_exp(rod_factory, dry_storage_exp_factory):
    material = rod_factory(_quantity=1)[0]
    rod = dry_storage_exp_factory(_quantity=5, material=material)
    rod_db = DryStorageExp.objects.get(id=rod[0].pk)
    rod_db.save()
    assert DryStorageExp.objects.get(id=rod[0].pk).updated_at != material.updated_at
    assert DryStorageExp.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_exp(dry_storage_exp_factory):
    rod = dry_storage_exp_factory(_quantity=1)
    DryStorageExp.objects.filter(id=rod[0].pk).delete()
    assert not DryStorageExp.objects.filter(id=rod[0].pk).exists()


@pytest.mark.django_db
def test_delete_test_with_material(dry_storage_exp_factory, rod_factory, material_factory):
    material = material_factory(_quantity=1)[0]
    fresh_rod = rod_factory(_quantity=1, material=material)[0]
    rod = dry_storage_exp_factory(_quantity=1, material=fresh_rod)[0]
    material.delete()
    assert not DryStorageExp.objects.filter(id=rod.pk).exists()