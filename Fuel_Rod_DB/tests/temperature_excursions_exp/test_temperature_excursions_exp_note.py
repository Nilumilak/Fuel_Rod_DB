import pytest

from temperature_excursions_exp.models import TemperatureExcursionExp, TemperatureExcursionExpNote


@pytest.mark.django_db
def test_create_note(temperature_excursions_exp_note_factory):
    """
    Create one TemperatureExcursionExpNote
    """
    note = temperature_excursions_exp_note_factory()

    assert TemperatureExcursionExpNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_create_notes(temperature_excursions_exp_note_factory):
    """
    Create many TemperatureExcursionExpNote
    """
    temperature_excursions_exp_note_factory(_quantity=5)

    assert TemperatureExcursionExpNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(temperature_excursions_exp_note_factory):
    """
    Update TemperatureExcursionExpNote
    """
    note = temperature_excursions_exp_note_factory()
    rod_note_db = TemperatureExcursionExpNote.objects.get(id=note.pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert TemperatureExcursionExpNote.objects.get(id=note.pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(temperature_excursions_exp_note_factory):
    """
    Delete TemperatureExcursionExpNote
    """
    note = temperature_excursions_exp_note_factory()
    TemperatureExcursionExpNote.objects.filter(id=note.pk).delete()

    assert not TemperatureExcursionExpNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(temperature_excursions_exp_note_factory, temperature_excursions_exp_factory):
    """
    TemperatureExcursionExpNote should automatically delete with its rod
    """
    rod = temperature_excursions_exp_factory()
    note = temperature_excursions_exp_note_factory(_quantity=5, rod=rod)
    TemperatureExcursionExp.objects.get(id=note[0].rod.pk).delete()

    assert not TemperatureExcursionExpNote.objects.all().exists()
