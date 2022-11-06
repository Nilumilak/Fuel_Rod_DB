import pytest

from temperature_excursions.models import RodTemperatureTest, RodTemperatureTestNote


@pytest.mark.django_db
def test_create_note(temperature_excursions_test_note_factory):
    """
    Create one RodTemperatureTestNote
    """
    note = temperature_excursions_test_note_factory()

    assert RodTemperatureTestNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_create_notes(temperature_excursions_test_note_factory):
    """
    Create many RodTemperatureTestNote
    """
    temperature_excursions_test_note_factory(_quantity=5)

    assert RodTemperatureTestNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(temperature_excursions_test_note_factory):
    """
    Update RodTemperatureTestNote
    """
    note = temperature_excursions_test_note_factory()
    rod_note_db = RodTemperatureTestNote.objects.get(id=note.pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert RodTemperatureTestNote.objects.get(id=note.pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(temperature_excursions_test_note_factory):
    """
    Delete RodTemperatureTestNote
    """
    note = temperature_excursions_test_note_factory()
    RodTemperatureTestNote.objects.filter(id=note.pk).delete()

    assert not RodTemperatureTestNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(temperature_excursions_test_note_factory, temperature_excursions_test_factory):
    """
    RodTemperatureTestNote should automatically delete with its rod
    """
    rod = temperature_excursions_test_factory(_quantity=1)[0]
    note = temperature_excursions_test_note_factory(_quantity=5, rod=rod)
    RodTemperatureTest.objects.get(id=note[0].rod.pk).delete()

    assert not RodTemperatureTestNote.objects.all().exists()