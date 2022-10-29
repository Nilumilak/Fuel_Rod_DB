import pytest

from temperature_excursions_exp.models import TemperatureExcursionExp, TemperatureExcursionExpNote


@pytest.mark.django_db
def test_create_note(temperature_excursions_exp_note_factory):
    note = temperature_excursions_exp_note_factory(_quantity=1)

    assert TemperatureExcursionExpNote.objects.filter(id=note[0].pk).exists()


@pytest.mark.django_db
def test_create_notes(temperature_excursions_exp_note_factory):
    temperature_excursions_exp_note_factory(_quantity=5)

    assert TemperatureExcursionExpNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(temperature_excursions_exp_note_factory):
    note = temperature_excursions_exp_note_factory(_quantity=1)
    rod_note_db = TemperatureExcursionExpNote.objects.get(id=note[0].pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert TemperatureExcursionExpNote.objects.get(id=note[0].pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(temperature_excursions_exp_note_factory):
    note = temperature_excursions_exp_note_factory(_quantity=1)
    TemperatureExcursionExpNote.objects.filter(id=note[0].pk).delete()

    assert not TemperatureExcursionExpNote.objects.filter(id=note[0].pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(temperature_excursions_exp_note_factory, temperature_excursions_exp_factory):
    rod = temperature_excursions_exp_factory(_quantity=1)[0]
    note = temperature_excursions_exp_note_factory(_quantity=5, rod=rod)
    TemperatureExcursionExp.objects.get(id=note[0].rod.pk).delete()

    assert not TemperatureExcursionExpNote.objects.all().exists()
