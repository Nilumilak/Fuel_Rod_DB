import pytest

from dry_storage.forms import CreateRodDryStorageTestForm

fixture = [
    (5, 5, 5, 5, 5, 5, 'test_note', True),
    ('5', '5', '5', '5', '5', '5', 'test_note', True),
    (5, '', 5, 5, 5, 5, 'test_note', False),
    (5, 'qwe', 5, 5, 5, 5, 'test_note', False),
    (5, 5, 5, 5, 5, 5, 'test_note\r\ntest_note', True),
]


@pytest.mark.parametrize(
    'original_length, heating_rate, cooling_rate, max_temperature, heating_time, cooling_time, notes, validity',
    fixture)
def test_form(original_length, heating_rate, cooling_rate,
              max_temperature, heating_time, cooling_time, notes, validity):
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

