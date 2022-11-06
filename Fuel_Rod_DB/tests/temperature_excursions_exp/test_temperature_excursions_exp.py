import pytest

from temperature_excursions_exp.models import TemperatureExcursionExp


@pytest.mark.django_db
def test_create_exp(temperature_excursions_exp_factory):
    """
    Create one TemperatureExcursionExp
    """
    rod = temperature_excursions_exp_factory()
    rod_db = TemperatureExcursionExp.objects.get(id=rod.pk)

    assert TemperatureExcursionExp.objects.filter(id=rod.pk).exists()
    assert rod_db.number == TemperatureExcursionExp.objects.filter(material__material=rod.material.material).count()
    assert rod_db.exp_id == f'{rod_db.material.material}-TE{"Q" if rod_db.quenched else ""}{rod_db.number:02}'


@pytest.mark.django_db
def test_create_exps(temperature_excursions_exp_factory):
    """
    Create many TemperatureExcursionExp
    """
    temperature_excursions_exp_factory(_quantity=5)

    assert TemperatureExcursionExp.objects.count() == 5
    assert list(TemperatureExcursionExp.objects.all()) == list(TemperatureExcursionExp.objects.all().order_by('exp_id'))


@pytest.mark.django_db
def test_create_exp_with_same_fresh_material(rod_factory, temperature_excursions_exp_factory):
    """
    Create many TemperatureExcursionExp with the same material and quench mode
    """
    material = rod_factory()
    rods = temperature_excursions_exp_factory(_quantity=2, material=material, quenched=True)

    # 'number' is auto-incrementing for rods with the same material
    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_create_exp_with_different_quench_mode(rod_factory, temperature_excursions_exp_factory):
    """
    Create many TemperatureExcursionExp with different quench mode
    """
    material = rod_factory()
    rod_1 = temperature_excursions_exp_factory(material=material, quenched=True)
    rod_2 = temperature_excursions_exp_factory(material=material, quenched=False)

    assert rod_1.number == rod_2.number
    assert rod_1.exp_id == f'{rod_1.material.material}-TEQ{rod_1.number:02}'
    assert rod_2.exp_id == f'{rod_2.material.material}-TE{rod_2.number:02}'


@pytest.mark.django_db
def test_update_exp(rod_factory, temperature_excursions_exp_factory):
    """
    Update TemperatureExcursionExp
    """
    material = rod_factory()
    rod = temperature_excursions_exp_factory(_quantity=5, material=material)
    rod_db = TemperatureExcursionExp.objects.get(id=rod[0].pk)
    rod_db.save()
    assert TemperatureExcursionExp.objects.get(id=rod[0].pk).updated_at != material.updated_at
    # 'number' should not change when updating
    assert TemperatureExcursionExp.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_exp(temperature_excursions_exp_factory):
    """
    Delete TemperatureExcursionExp
    """
    rod = temperature_excursions_exp_factory()
    TemperatureExcursionExp.objects.filter(id=rod.pk).delete()
    assert not TemperatureExcursionExp.objects.filter(id=rod.pk).exists()


@pytest.mark.django_db
def test_delete_test_with_material(temperature_excursions_exp_factory, rod_factory, material_factory):
    """
    TemperatureExcursionExp should automatically delete with its material
    """
    material = material_factory()
    fresh_rod = rod_factory(material=material)
    rod = temperature_excursions_exp_factory(material=fresh_rod)
    material.delete()
    assert not TemperatureExcursionExp.objects.filter(id=rod.pk).exists()