import pytest

from dry_storage_exp.models import DryStorageExp


@pytest.mark.django_db
def test_create_exp(dry_storage_exp_factory):
    """
    Create one DryStorageExp
    """
    rod = dry_storage_exp_factory()
    rod_db = DryStorageExp.objects.get(id=rod.pk)

    assert DryStorageExp.objects.filter(id=rod.pk).exists()
    assert rod_db.number == DryStorageExp.objects.filter(material__material=rod.material.material).count()
    assert rod_db.exp_id == f'{rod.material.material}-DS{rod.number:02}'


@pytest.mark.django_db
def test_create_exps(dry_storage_exp_factory):
    """
    Create many DryStorageExp
    """
    dry_storage_exp_factory(_quantity=5)

    assert DryStorageExp.objects.count() == 5
    assert list(DryStorageExp.objects.all()) == list(DryStorageExp.objects.all().order_by('exp_id'))


@pytest.mark.django_db
def test_create_exp_with_same_fresh_material(rod_factory, dry_storage_exp_factory):
    """
    Create many DryStorageExp with the same material
    """
    material = rod_factory()
    rods = dry_storage_exp_factory(_quantity=2, material=material)

    # 'number' is auto-incrementing for rods with the same material
    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_update_exp(rod_factory, dry_storage_exp_factory):
    """
    Update DryStorageExp
    """
    material = rod_factory()
    rod = dry_storage_exp_factory(_quantity=5, material=material)
    rod_db = DryStorageExp.objects.get(id=rod[0].pk)
    rod_db.save()
    assert DryStorageExp.objects.get(id=rod[0].pk).updated_at != material.updated_at
    # 'number' should not change when updating
    assert DryStorageExp.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_exp(dry_storage_exp_factory):
    """
    Delete DryStorageExp
    """
    rod = dry_storage_exp_factory()
    DryStorageExp.objects.filter(id=rod.pk).delete()
    assert not DryStorageExp.objects.filter(id=rod.pk).exists()


@pytest.mark.django_db
def test_delete_test_with_material(dry_storage_exp_factory, rod_factory, material_factory):
    """
    DryStorageExp should automatically delete with its material
    """
    material = material_factory()
    fresh_rod = rod_factory(material=material)
    rod = dry_storage_exp_factory(material=fresh_rod)
    material.delete()
    assert not DryStorageExp.objects.filter(id=rod.pk).exists()
