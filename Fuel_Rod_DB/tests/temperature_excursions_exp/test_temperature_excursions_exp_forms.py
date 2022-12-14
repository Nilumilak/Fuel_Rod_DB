import pytest

from temperature_excursions_exp.forms import CreateTemperatureExcursionExpForm, UpdateTemperatureExcursionExpForm
from fresh_inventory.models import RawRod


fixture = [
    # all correct
    (True, 'test_note', True),
    # more than one note
    (False, 'test_note_1\r\ntest_note_2', True),
    # int instead of bool
    (1, 123, True),
    # str instead of bool
    ('1', '', True),
]


@pytest.mark.django_db
@pytest.mark.parametrize('quenched, notes, validity', fixture)
def test_create_form(quenched, notes, validity, rod_factory):
    """
    CreateTemperatureExcursionExpForm test
    """
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


fixture = [
    # all correct
    ('test_note', True),
    # more than one note
    ('test_note_1\r\ntest_note_2', True),
    # int instead of bool
    (123, True),
    # field is not required
    ('', True),
]


@pytest.mark.django_db
@pytest.mark.parametrize('notes, validity', fixture)
def test_update_form(notes, validity, rod_factory):
    """
    UpdateTemperatureExcursionExpForm test
    """
    form = UpdateTemperatureExcursionExpForm(data={
        'notes': notes
    })

    assert form.is_valid() == validity
    assert type(form.cleaned_data['notes']) == list
    assert form.cleaned_data['notes'] == str(notes).split('\r\n')
