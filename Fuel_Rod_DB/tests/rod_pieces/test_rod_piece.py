import pytest

from rod_pieces.models import RodPiece


@pytest.mark.django_db
def test_create_rod_piece(rod_piece_factory, sample_state_factory):
    """
    Create one RodPiece
    """
    rod = rod_piece_factory()
    rod_db = RodPiece.objects.get(id=rod.pk)

    assert RodPiece.objects.filter(id=rod.pk).exists()
    assert rod_db.number == RodPiece.objects.filter(material=rod.material, analysis_technique=rod.analysis_technique).count()
    assert rod_db.rod_id == f'{rod.material}-{rod.analysis_technique}{rod.number:02}'


@pytest.mark.django_db
def test_create_rod_pieces(rod_piece_factory):
    """
    Create many RodPiece
    """
    rod_piece_factory(_quantity=5)

    assert RodPiece.objects.count() == 5
    assert list(RodPiece.objects.all()) == list(RodPiece.objects.all().order_by('rod_id'))


@pytest.mark.django_db
def test_create_rod_pieces_same_material_and_same_analysis_technique(rod_piece_factory, analysis_technique_factory):
    """
    Create many RodPiece with the same material and analysis_technique
    """
    technique = analysis_technique_factory()
    material = 'test_material'
    rods = rod_piece_factory(_quantity=2, material=material, analysis_technique=technique)

    # 'number' is auto-incrementing for rods with the same material and analysis_technique
    assert rods[0].number == rods[1].number - 1


@pytest.mark.django_db
def test_create_rod_pieces_same_material_and_different_analysis_technique(rod_piece_factory, analysis_technique_factory):
    """
    Create many RodPiece with the same material and different analysis technique
    """
    technique = analysis_technique_factory(_quantity=2)
    material = 'test_material'
    rod_1 = rod_piece_factory(material=material, analysis_technique=technique[0])
    rod_2 = rod_piece_factory(material=material, analysis_technique=technique[1])

    assert rod_1.number == rod_2.number


@pytest.mark.django_db
def test_create_rod_pieces_different_material(rod_piece_factory):
    """
    Create many RodPiece with different material
    """
    material_1 = 'test_material_1'
    material_2 = 'test_material_2'
    rod_1 = rod_piece_factory(material=material_1)
    rod_2 = rod_piece_factory(material=material_2)

    assert rod_1.number == rod_2.number


@pytest.mark.django_db
def test_update_rod_piece(rod_piece_factory, analysis_technique_factory):
    """
    Update RodPiece
    """
    technique = analysis_technique_factory()
    material = 'test_material'
    rod = rod_piece_factory(_quantity=5, material=material, analysis_technique=technique)
    rod_db = RodPiece.objects.get(id=rod[0].pk)
    rod_db.save()
    assert RodPiece.objects.get(id=rod[0].pk).updated_at != rod[0].updated_at
    # 'number' should not change when updating
    assert RodPiece.objects.get(id=rod[0].pk).number == rod[0].number


@pytest.mark.django_db
def test_delete_rod_piece(rod_piece_factory):
    """
    Delete RodPiece
    """
    rod = rod_piece_factory()
    RodPiece.objects.filter(id=rod.pk).delete()
    assert not RodPiece.objects.filter(id=rod.pk).exists()


@pytest.mark.django_db
def test_delete_test_with_analysis_technique(rod_piece_factory, analysis_technique_factory):
    """
    RodPiece should automatically delete with its analysis_technique
    """
    technique = analysis_technique_factory()
    rod = rod_piece_factory(_quantity=5, analysis_technique=technique)[0]
    technique.delete()
    assert not RodPiece.objects.filter(id=rod.pk).exists()


@pytest.mark.django_db
def test_delete_test_with_sample_state(rod_piece_factory, sample_state_factory):
    """
    RodPiece should automatically delete with its sample_state
    """
    sample_state = sample_state_factory()
    rod = rod_piece_factory(_quantity=5, sample_state=sample_state)[0]
    sample_state.delete()
    assert not RodPiece.objects.filter(id=rod.pk).exists()


@pytest.mark.django_db
def test_delete_test_with_original_material(material_factory, rod_piece_factory,
                                            temperature_excursions_test_factory, dry_storage_test_factory):
    """
    RodPiece should automatically delete with its temperature_excursion_test or dry_storage_test
    """
    material = material_factory()
    raw_rod_1 = temperature_excursions_test_factory(raw_rod__material__material=material)
    raw_rod_2 = dry_storage_test_factory(raw_rod__material__material=material)

    rod_1 = rod_piece_factory(material=raw_rod_1.rod_id)
    rod_2 = rod_piece_factory(material=raw_rod_2.rod_id)

    material.delete()

    assert not RodPiece.objects.filter(rod_id=rod_1.rod_id).exists()
    assert not RodPiece.objects.filter(rod_id=rod_2.rod_id).exists()
