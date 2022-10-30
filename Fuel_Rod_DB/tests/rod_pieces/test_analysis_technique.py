import pytest
from django.db import IntegrityError

from rod_pieces.models import AnalysisTechnique


@pytest.mark.django_db
def test_create_material(analysis_technique_factory):
    material = analysis_technique_factory(_quantity=1)

    assert AnalysisTechnique.objects.filter(id=material[0].pk).exists()


@pytest.mark.django_db
def test_create_materials(analysis_technique_factory):
    analysis_technique_factory(_quantity=5)

    assert AnalysisTechnique.objects.count() == 5


@pytest.mark.django_db
def test_update_material(analysis_technique_factory):
    material = analysis_technique_factory(_quantity=1)
    material_db = AnalysisTechnique.objects.get(id=material[0].pk)
    material_db.name = 'test'
    material_db.save()

    assert AnalysisTechnique.objects.get(id=material[0].pk).name == 'test'


@pytest.mark.django_db
def test_delete_material(analysis_technique_factory):
    material = analysis_technique_factory(_quantity=1)
    AnalysisTechnique.objects.filter(id=material[0].pk).delete()

    assert not AnalysisTechnique.objects.filter(id=material[0].pk).exists()


@pytest.mark.django_db
def test_create_materials_name_unique_constraint(analysis_technique_factory):
    material = analysis_technique_factory(_quantity=1)

    try:
        AnalysisTechnique.objects.create(name=material[0].name)
        assert False
    except IntegrityError:
        assert True

