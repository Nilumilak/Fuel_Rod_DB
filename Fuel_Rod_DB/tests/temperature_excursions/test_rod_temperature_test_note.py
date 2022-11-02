import pytest

from temperature_excursions.models import RodTemperatureTest, RodTemperatureTestNote


@pytest.mark.django_db
def test_create_note(temperature_excursions_test_note_factory):
    note = temperature_excursions_test_note_factory(_quantity=1)

    assert RodTemperatureTestNote.objects.filter(id=note[0].pk).exists()


@pytest.mark.django_db
def test_create_notes(temperature_excursions_test_note_factory):
    temperature_excursions_test_note_factory(_quantity=5)

    assert RodTemperatureTestNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(temperature_excursions_test_note_factory):
    note = temperature_excursions_test_note_factory(_quantity=1)
    rod_note_db = RodTemperatureTestNote.objects.get(id=note[0].pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert RodTemperatureTestNote.objects.get(id=note[0].pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(temperature_excursions_test_note_factory):
    note = temperature_excursions_test_note_factory(_quantity=1)
    RodTemperatureTestNote.objects.filter(id=note[0].pk).delete()

    assert not RodTemperatureTestNote.objects.filter(id=note[0].pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(temperature_excursions_test_note_factory, temperature_excursions_test_factory):
    rod = temperature_excursions_test_factory(_quantity=1)[0]
    note = temperature_excursions_test_note_factory(_quantity=5, rod=rod)
    RodTemperatureTest.objects.get(id=note[0].rod.pk).delete()

    assert not RodTemperatureTestNote.objects.all().exists()