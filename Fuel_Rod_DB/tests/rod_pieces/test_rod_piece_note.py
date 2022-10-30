import pytest

from rod_pieces.models import RodPiece, RodPieceNote


@pytest.mark.django_db
def test_create_note(rod_piece_note_factory):
    note = rod_piece_note_factory(_quantity=1)

    assert RodPieceNote.objects.filter(id=note[0].pk).exists()


@pytest.mark.django_db
def test_create_notes(rod_piece_note_factory):
    rod_piece_note_factory(_quantity=5)

    assert RodPieceNote.objects.count() == 5


@pytest.mark.django_db
def test_update_note(rod_piece_note_factory):
    note = rod_piece_note_factory(_quantity=1)
    rod_note_db = RodPieceNote.objects.get(id=note[0].pk)
    rod_note_db.text = 'test'
    rod_note_db.save()

    assert RodPieceNote.objects.get(id=note[0].pk).text == 'test'


@pytest.mark.django_db
def test_delete_note(rod_piece_note_factory):
    note = rod_piece_note_factory(_quantity=1)
    RodPieceNote.objects.filter(id=note[0].pk).delete()

    assert not RodPieceNote.objects.filter(id=note[0].pk).exists()


@pytest.mark.django_db
def test_delete_note_with_rod(rod_piece_note_factory, rod_piece_factory):
    rod = rod_piece_factory(_quantity=1)[0]
    note = rod_piece_note_factory(_quantity=5, rod=rod)
    RodPiece.objects.get(id=note[0].rod.pk).delete()

    assert not RodPieceNote.objects.all().exists()
