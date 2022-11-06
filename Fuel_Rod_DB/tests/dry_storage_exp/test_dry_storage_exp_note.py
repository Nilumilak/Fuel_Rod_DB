import pytest

from dry_storage_exp.models import DryStorageExp, DryStorageExpNote


@pytest.mark.django_db
def test_create_note(dry_storage_exp_note_factory):
    """
    Create one DryStorageExpNote
    """
    note = dry_storage_exp_note_factory()

    assert DryStorageExpNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_create_notes(dry_storage_exp_note_factory):
    """
    Create many DryStorageExpNote
    """
    dry_storage_exp_note_factory(_quantity=5)

    assert DryStorageExpNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(dry_storage_exp_note_factory):
    """
    Update DryStorageExpNote
    """
    note = dry_storage_exp_note_factory()
    rod_note_db = DryStorageExpNote.objects.get(id=note.pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert DryStorageExpNote.objects.get(id=note.pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(dry_storage_exp_note_factory):
    """
    Delete DryStorageExpNote
    """
    note = dry_storage_exp_note_factory()
    DryStorageExpNote.objects.filter(id=note.pk).delete()

    assert not DryStorageExpNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(dry_storage_exp_note_factory, dry_storage_exp_factory):
    """
    DryStorageExpNote should automatically delete with its rod
    """
    rod = dry_storage_exp_factory()
    note = dry_storage_exp_note_factory(_quantity=5, rod=rod)
    DryStorageExp.objects.get(id=note[0].rod.pk).delete()

    assert not DryStorageExpNote.objects.all().exists()
