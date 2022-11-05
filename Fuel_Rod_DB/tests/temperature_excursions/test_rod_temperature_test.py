import pytest

from fresh_inventory.models import RawRod
from temperature_excursions.models import RodTemperatureTest


@pytest.mark.django_db
def test_create_test(temperature_excursions_test_factory):
    rod = temperature_excursions_test_factory(_quantity=1)
    rod_db = RodTemperatureTest.objects.get(id=rod[0].pk)

    assert RodTemperatureTest.objects.filter(id=rod[0].pk).exists()
    assert rod_db.number == RodTemperatureTest.objects.filter(raw_rod=rod_db.raw_rod).count()
    assert rod_db.rod_id == f'{rod_db.raw_rod.exp_id}-R{rod_db.number:02}'


@pytest.mark.django_db
def test_create_tests(temperature_excursions_test_factory):
    temperature_excursions_test_factory(_quantity=5)

    assert RodTemperatureTest.objects.count() == 5
    assert list(RodTemperatureTest.objects.all()) == list(RodTemperatureTest.objects.all().order_by('rod_id'))


@pytest.mark.django_db
def test_create_test_with_same_fresh_material(temperature_excursions_test_factory, temperature_excursions_exp_factory):
    raw_rod = temperature_excursions_exp_factory(_quantity=1)[0]
    rods = temperature_excursions_test_factory(_quantity=2, raw_rod=raw_rod)

    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_update_test(temperature_excursions_test_factory, temperature_excursions_exp_factory):
    raw_rod = temperature_excursions_exp_factory(_quantity=1)[0]
    rod = temperature_excursions_test_factory(_quantity=5, raw_rod=raw_rod)
    rod_db = RodTemperatureTest.objects.get(id=rod[0].pk)
    rod_db.original_length = 1
    rod_db.save()
    assert RodTemperatureTest.objects.get(id=rod[0].pk).original_length == 1
    assert RodTemperatureTest.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_test(temperature_excursions_test_factory):
    rod = temperature_excursions_test_factory()
    length = rod.raw_rod.material.length
    RodTemperatureTest.objects.filter(id=rod.pk).delete()
    assert not RodTemperatureTest.objects.filter(id=rod.pk).exists()
    assert RawRod.objects.get(id=rod.raw_rod.material.pk).length == length + rod.original_length


@pytest.mark.django_db
def test_delete_test_with_material(temperature_excursions_test_factory, temperature_excursions_exp_factory, rod_factory, material_factory):
    material = material_factory(_quantity=1)[0]
    fresh_rod = rod_factory(_quantity=1, material=material)[0]
    raw_rod = temperature_excursions_exp_factory(_quantity=1, material=fresh_rod)[0]
    rod = temperature_excursions_test_factory(_quantity=1, raw_rod=raw_rod)
    material.delete()
    assert not RodTemperatureTest.objects.filter(id=rod[0].pk).exists()