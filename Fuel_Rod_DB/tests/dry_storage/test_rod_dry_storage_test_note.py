import pytest

from dry_storage.models import RodDryStorageTest, RodDryStorageTestNote


@pytest.mark.django_db
def test_create_note(dry_storage_test_note_factory):
    """
    Create one RodDryStorageTestNote
    """
    note = dry_storage_test_note_factory()

    assert RodDryStorageTestNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_create_notes(dry_storage_test_note_factory):
    """
    Create many RodDryStorageTestNote
    """
    dry_storage_test_note_factory(_quantity=5)

    assert RodDryStorageTestNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(dry_storage_test_note_factory):
    """
    Update RodDryStorageTestNote
    """
    note = dry_storage_test_note_factory()
    rod_note_db = RodDryStorageTestNote.objects.get(id=note.pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert RodDryStorageTestNote.objects.get(id=note.pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(dry_storage_test_note_factory):
    """
    Delete RodDryStorageTestNote
    """
    note = dry_storage_test_note_factory()
    RodDryStorageTestNote.objects.filter(id=note.pk).delete()

    assert not RodDryStorageTestNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(dry_storage_test_note_factory, dry_storage_test_factory):
    """
    RodDryStorageTestNote should automatically delete with its rod
    """
    rod = dry_storage_test_factory()
    note = dry_storage_test_note_factory(rod=rod)
    RodDryStorageTest.objects.get(id=note.rod.pk).delete()

    assert not RodDryStorageTestNote.objects.all().exists()
