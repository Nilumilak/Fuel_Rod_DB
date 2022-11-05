import pytest

from rod_pieces.models import RodPiece


@pytest.mark.django_db
def test_create_rod_piece(rod_piece_factory, sample_state_factory):
    rod = rod_piece_factory(_quantity=1)[0]
    rod_db = RodPiece.objects.get(id=rod.pk)

    assert RodPiece.objects.filter(id=rod.pk).exists()
    assert rod_db.number == RodPiece.objects.filter(material=rod.material, analysis_technique=rod.analysis_technique).count()
    assert rod_db.rod_id == f'{rod.material}-{rod.analysis_technique}{rod.number:02}'


@pytest.mark.django_db
def test_create_rod_pieces(rod_piece_factory):
    rod_piece_factory(_quantity=5)

    assert RodPiece.objects.count() == 5
    assert list(RodPiece.objects.all()) == list(RodPiece.objects.all().order_by('rod_id'))


@pytest.mark.django_db
def test_create_rod_pieces_same_material_and_same_analysis_technique(rod_piece_factory, analysis_technique_factory):
    technique = analysis_technique_factory(_quantity=1)[0]
    material = 'test_material'
    rods = rod_piece_factory(_quantity=2, material=material, analysis_technique=technique)

    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_create_rod_pieces_same_material_and_different_analysis_technique(rod_piece_factory, analysis_technique_factory):
    technique = analysis_technique_factory(_quantity=2)
    material = 'test_material'
    rod_1 = rod_piece_factory(_quantity=1, material=material, analysis_technique=technique[0])
    rod_2 = rod_piece_factory(_quantity=1, material=material, analysis_technique=technique[1])

    assert rod_1[0].number == rod_2[0].number


@pytest.mark.django_db
def test_create_rod_pieces_different_material(rod_piece_factory):
    material_1 = 'test_material_1'
    material_2 = 'test_material_2'
    rod_1 = rod_piece_factory(_quantity=1, material=material_1)[0]
    rod_2 = rod_piece_factory(_quantity=1, material=material_2)[0]

    assert rod_1.number == rod_2.number


@pytest.mark.django_db
def test_update_rod_piece(rod_piece_factory, analysis_technique_factory):
    technique = analysis_technique_factory(_quantity=1)[0]
    material = 'test_material'
    rod = rod_piece_factory(_quantity=5, material=material, analysis_technique=technique)
    rod_db = RodPiece.objects.get(id=rod[0].pk)
    rod_db.save()
    assert RodPiece.objects.get(id=rod[0].pk).updated_at != rod[0].updated_at
    assert RodPiece.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_rod_piece(rod_piece_factory):
    rod = rod_piece_factory(_quantity=1)
    RodPiece.objects.filter(id=rod[0].pk).delete()
    assert not RodPiece.objects.filter(id=rod[0].pk).exists()


@pytest.mark.django_db
def test_delete_test_with_analysis_technique(rod_piece_factory, analysis_technique_factory):
    technique = analysis_technique_factory(_quantity=1)[0]
    rod = rod_piece_factory(_quantity=5, analysis_technique=technique)[0]
    technique.delete()
    assert not RodPiece.objects.filter(id=rod.pk).exists()


@pytest.mark.django_db
def test_delete_test_with_sample_state(rod_piece_factory, sample_state_factory):
    sample_state = sample_state_factory(_quantity=1)[0]
    rod = rod_piece_factory(_quantity=5, sample_state=sample_state)[0]
    sample_state.delete()
    assert not RodPiece.objects.filter(id=rod.pk).exists()