import pytest

from rod_pieces.forms import CreateRodPieceForm
from rod_pieces.models import SampleState, AnalysisTechnique


fixture = [
    ('test_note', True),
    ('test_note_1\r\ntest_note_2', True),
    (123, True),
    ('', True),
]


@pytest.mark.django_db
@pytest.mark.parametrize('notes, validity', fixture)
def test_form(notes, validity, sample_state_factory, analysis_technique_factory):
    technique = analysis_technique_factory()
    sample = sample_state_factory()
    form = CreateRodPieceForm(data={
        'analysis_technique': technique,
        'sample_state': sample,
        'notes': notes
    })
    form.save()
    assert form.is_valid() == validity
    assert type(form.cleaned_data['analysis_technique']) == AnalysisTechnique
    assert type(form.cleaned_data['sample_state']) == SampleState
    assert type(form.cleaned_data['notes']) == list
    assert form.cleaned_data['notes'] == str(notes).split('\r\n')
