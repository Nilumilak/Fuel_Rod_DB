import pytest

from fresh_inventory.models import RawRodNote, RawRod


@pytest.mark.django_db
def test_create_note(note_factory):
    note = note_factory(_quantity=1)

    assert RawRodNote.objects.filter(id=note[0].pk).exists()


@pytest.mark.django_db
def test_create_notes(note_factory):
    note_factory(_quantity=5)

    assert RawRodNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(note_factory):
    note = note_factory(_quantity=1)
    rod_note_db = RawRodNote.objects.get(id=note[0].pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert RawRodNote.objects.get(id=note[0].pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(note_factory):
    note = note_factory(_quantity=1)
    RawRodNote.objects.filter(id=note[0].pk).delete()

    assert not RawRodNote.objects.filter(id=note[0].pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(note_factory):
    note = note_factory(_quantity=1)
    RawRod.objects.get(id=note[0].rod.pk).delete()

    assert not RawRodNote.objects.all().exists()
