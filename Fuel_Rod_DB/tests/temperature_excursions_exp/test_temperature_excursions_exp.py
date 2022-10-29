import pytest

from temperature_excursions_exp.models import TemperatureExcursionExp


@pytest.mark.django_db
def test_create_exp(temperature_excursions_exp_factory):
    rod = temperature_excursions_exp_factory(_quantity=1)[0]
    rod_db = TemperatureExcursionExp.objects.get(id=rod.pk)

    assert TemperatureExcursionExp.objects.filter(id=rod.pk).exists()
    assert rod_db.number == TemperatureExcursionExp.objects.filter(material__material=rod.material.material).count()
    assert rod_db.exp_id == f'{rod_db.material.material}-TE{"Q" if rod_db.quenched else ""}{rod_db.number:02}'


@pytest.mark.django_db
def test_create_exp(temperature_excursions_exp_factory):
    temperature_excursions_exp_factory(_quantity=5)

    assert TemperatureExcursionExp.objects.count() == 5
    assert list(TemperatureExcursionExp.objects.all()) == list(TemperatureExcursionExp.objects.all().order_by('exp_id'))


@pytest.mark.django_db
def test_create_exp_with_same_fresh_material(rod_factory, temperature_excursions_exp_factory):
    material = rod_factory(_quantity=1)[0]
    rods = temperature_excursions_exp_factory(_quantity=2, material=material, quenched=True)

    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_create_exp_with_different_quench_mode(rod_factory, temperature_excursions_exp_factory):
    material = rod_factory(_quantity=1)[0]
    rod_1 = temperature_excursions_exp_factory(_quantity=1, material=material, quenched=True)[0]
    rod_2 = temperature_excursions_exp_factory(_quantity=1, material=material, quenched=False)[0]

    assert rod_1.number == rod_2.number
    assert rod_1.exp_id == f'{rod_1.material.material}-TEQ{rod_1.number:02}'
    assert rod_2.exp_id == f'{rod_2.material.material}-TE{rod_2.number:02}'


@pytest.mark.django_db
def test_update_exp(rod_factory, temperature_excursions_exp_factory):
    material = rod_factory(_quantity=1)[0]
    rod = temperature_excursions_exp_factory(_quantity=5, material=material)
    rod_db = TemperatureExcursionExp.objects.get(id=rod[0].pk)
    rod_db.save()
    assert TemperatureExcursionExp.objects.get(id=rod[0].pk).updated_at != material.updated_at
    assert TemperatureExcursionExp.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_exp(temperature_excursions_exp_factory):
    rod = temperature_excursions_exp_factory(_quantity=1)
    TemperatureExcursionExp.objects.filter(id=rod[0].pk).delete()
    assert not TemperatureExcursionExp.objects.filter(id=rod[0].pk).exists()


@pytest.mark.django_db
def test_delete_test_with_material(temperature_excursions_exp_factory, rod_factory, material_factory):
    material = material_factory(_quantity=1)[0]
    fresh_rod = rod_factory(_quantity=1, material=material)[0]
    rod = temperature_excursions_exp_factory(_quantity=1, material=fresh_rod)[0]
    material.delete()
    assert not TemperatureExcursionExp.objects.filter(id=rod.pk).exists()