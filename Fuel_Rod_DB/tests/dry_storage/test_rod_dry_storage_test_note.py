import pytest

from dry_storage.models import RodDryStorageTest, RodDryStorageTestNote


@pytest.mark.django_db
def test_create_note(dry_storage_test_note_factory):
    note = dry_storage_test_note_factory(_quantity=1)

    assert RodDryStorageTestNote.objects.filter(id=note[0].pk).exists()


@pytest.mark.django_db
def test_create_notes(dry_storage_test_note_factory):
    dry_storage_test_note_factory(_quantity=5)

    assert RodDryStorageTestNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(dry_storage_test_note_factory):
    note = dry_storage_test_note_factory(_quantity=1)
    rod_note_db = RodDryStorageTestNote.objects.get(id=note[0].pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert RodDryStorageTestNote.objects.get(id=note[0].pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(dry_storage_test_note_factory):
    note = dry_storage_test_note_factory(_quantity=1)
    RodDryStorageTestNote.objects.filter(id=note[0].pk).delete()

    assert not RodDryStorageTestNote.objects.filter(id=note[0].pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(dry_storage_test_note_factory):
    note = dry_storage_test_note_factory(_quantity=1)
    RodDryStorageTest.objects.get(id=note[0].rod.pk).delete()

    assert not RodDryStorageTestNote.objects.all().exists()
