import pytest

from fresh_inventory.models import RawRodNote, RawRod


@pytest.mark.django_db
def test_create_note(note_factory):
    """
    Create one RawRodNote
    """
    note = note_factory()

    assert RawRodNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_create_notes(note_factory):
    """
    Create many RawRodNote
    """
    note_factory(_quantity=5)

    assert RawRodNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(note_factory):
    """
    Update RawRodNote
    """
    note = note_factory()
    rod_note_db = RawRodNote.objects.get(id=note.pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert RawRodNote.objects.get(id=note.pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(note_factory):
    """
    Delete RawRodNote
    """
    note = note_factory()
    RawRodNote.objects.filter(id=note.pk).delete()

    assert not RawRodNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(note_factory):
    """
    RawRodNote should automatically delete with its rod
    """
    note = note_factory()
    RawRod.objects.get(id=note.rod.pk).delete()

    assert not RawRodNote.objects.all().exists()
