import pytest

from rod_pieces.models import RodPiece, RodPieceNote


@pytest.mark.django_db
def test_create_note(rod_piece_note_factory):
    """
    Create one RodPieceNote
    """
    note = rod_piece_note_factory()

    assert RodPieceNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_create_notes(rod_piece_note_factory):
    """
    Create many RodPieceNote
    """
    rod_piece_note_factory(_quantity=5)

    assert RodPieceNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(rod_piece_note_factory):
    """
    Update RodPieceNote
    """
    note = rod_piece_note_factory()
    rod_note_db = RodPieceNote.objects.get(id=note.pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert RodPieceNote.objects.get(id=note.pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(rod_piece_note_factory):
    """
    Delete RodPieceNote
    """
    note = rod_piece_note_factory()
    RodPieceNote.objects.filter(id=note.pk).delete()

    assert not RodPieceNote.objects.filter(id=note.pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(rod_piece_note_factory, rod_piece_factory):
    """
    RodPieceNote should automatically delete with its rod
    """
    rod = rod_piece_factory()
    note = rod_piece_note_factory(_quantity=5, rod=rod)
    RodPiece.objects.get(id=note[0].rod.pk).delete()

    assert not RodPieceNote.objects.all().exists()
