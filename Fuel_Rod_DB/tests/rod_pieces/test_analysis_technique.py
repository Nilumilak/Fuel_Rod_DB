import pytest
from django.db import IntegrityError

from rod_pieces.models import AnalysisTechnique


@pytest.mark.django_db
def test_create_analysis_technique(analysis_technique_factory):
    """
    Create one AnalysisTechnique
    """
    material = analysis_technique_factory()

    assert AnalysisTechnique.objects.filter(id=material.pk).exists()


@pytest.mark.django_db
def test_create_analysis_techniques(analysis_technique_factory):
    """
    Create many AnalysisTechnique
    """
    analysis_technique_factory(_quantity=5)

    assert AnalysisTechnique.objects.count() == 5


@pytest.mark.django_db
def test_update_analysis_technique(analysis_technique_factory):
    """
    Update AnalysisTechnique
    """
    material = analysis_technique_factory()
    material_db = AnalysisTechnique.objects.get(id=material.pk)
    material_db.name = 'test'
    material_db.save()

    assert AnalysisTechnique.objects.get(id=material.pk).name == 'test'


@pytest.mark.django_db
def test_delete_analysis_technique(analysis_technique_factory):
    """
    Delete AnalysisTechnique
    """
    material = analysis_technique_factory()
    AnalysisTechnique.objects.filter(id=material.pk).delete()

    assert not AnalysisTechnique.objects.filter(id=material.pk).exists()


@pytest.mark.django_db
def test_create_analysis_technique_name_unique_constraint(analysis_technique_factory):
    """
    AnalysisTechnique name should be unique
    """
    material = analysis_technique_factory()

    try:
        AnalysisTechnique.objects.create(name=material.name)
        assert False
    except IntegrityError:
        assert True

