import pytest

from temperature_excursions_exp.forms import CreateTemperatureExcursionExpForm
from fresh_inventory.models import RawRod


fixture = [
    (True, 'test_note', True),
    (False, 'test_note_1\r\ntest_note_2', True),
    (1, 123, True),
    ('1', '', True),
]


@pytest.mark.django_db
@pytest.mark.parametrize('quenched, notes, validity', fixture)
def test_form(quenched, notes, validity, rod_factory):
    material = rod_factory()
    form = CreateTemperatureExcursionExpForm(data={
        'material': material,
        'quenched': quenched,
        'notes': notes
    })
    assert form.is_valid() == validity
    assert type(form.cleaned_data['quenched']) == bool
    assert type(form.cleaned_data['material']) == RawRod
    assert type(form.cleaned_data['notes']) == list
    assert form.cleaned_data['notes'] == str(notes).split('\r\n')
