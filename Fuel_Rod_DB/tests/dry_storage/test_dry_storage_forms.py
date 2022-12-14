import pytest

from dry_storage.forms import CreateRodDryStorageTestForm, UpdateRodDryStorageTestForm

fixture = [
    # all correct
    (5, 5, 5, 5, 5, 5, 'test_note', True),
    # all correct
    ('5', '5', '5', '5', '5', '5', 'test_note', True),
    # fields are not required
    ('', '', '', '', '', '', 'test_note', True),
    # only digits are allowed for the field
    (5, 'qwe', 5, 5, 5, 5, 'test_note', False),
    # more than one note
    (5, 5, 5, 5, 5, 5, 'test_note\r\ntest_note', True),
]


@pytest.mark.parametrize(
    'original_length, heating_rate, cooling_rate, max_temperature, heating_time, cooling_time, notes, validity',
    fixture)
def test_create_form(original_length, heating_rate, cooling_rate, max_temperature, heating_time, cooling_time, notes, validity):
    """
    CreateRodDryStorageTestForm test
    """
    form = CreateRodDryStorageTestForm(data={
        'original_length': original_length,
        'heating_rate': heating_rate,
        'cooling_rate': cooling_rate,
        'max_temperature': max_temperature,
        'heating_time': heating_time,
        'cooling_time': cooling_time,
        'notes': notes
    })
    assert form.is_valid() == validity
    assert type(form.cleaned_data['notes']) == list
    assert form.cleaned_data['notes'] == str(notes).split('\r\n')


fixture = [
    # all correct
    (5, 5, 5, 5, 5, 5, 'test_note', True),
    # all correct
    ('5', '5', '5', '5', '5', '5', 'test_note', True),
    # fields are not required
    ('', '', '', '', '', '', 'test_note', True),
    # only digits are allowed for the field
    (5, 'qwe', 5, 5, 5, 5, 'test_note', False),
    # more than one note
    (5, 5, 5, 5, 5, 5, 'test_note\r\ntest_note', True),
]


@pytest.mark.parametrize(
    'original_length, heating_rate, cooling_rate, max_temperature, heating_time, cooling_time, notes, validity',
    fixture)
def test_update_form(original_length, heating_rate, cooling_rate, max_temperature, heating_time, cooling_time, notes, validity):
    """
    UpdateRodDryStorageTestForm test
    """
    form = UpdateRodDryStorageTestForm(data={
        'original_length': original_length,
        'heating_rate': heating_rate,
        'cooling_rate': cooling_rate,
        'max_temperature': max_temperature,
        'heating_time': heating_time,
        'cooling_time': cooling_time,
        'notes': notes
    })
    assert form.is_valid() == validity
    assert type(form.cleaned_data['notes']) == list
    assert form.cleaned_data['notes'] == str(notes).split('\r\n')

