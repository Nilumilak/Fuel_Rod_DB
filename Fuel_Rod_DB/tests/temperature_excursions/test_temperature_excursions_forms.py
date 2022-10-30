import pytest

from temperature_excursions.forms import CreateRodTemperatureTestForm

fixture = [
    (5, 5, 5, 5, 'test_note', True),
    ('5', '5', '5', '5', 'test_note', True),
    (5, '', 5, 5, 'test_note', False),
    (5, 'qwe', 5, 5, 'test_note', False),
    (5, 5, 5, 5, 'test_note\r\ntest_note', True),
]


@pytest.mark.parametrize(
    'original_length, power, max_temperature, heating_time, notes, validity',
    fixture)
def test_form(original_length, power, max_temperature, heating_time, notes, validity):
    form = CreateRodTemperatureTestForm(data={
        'original_length': original_length,
        'power': power,
        'max_temperature': max_temperature,
        'heating_time': heating_time,
        'notes': notes
    })
    assert form.is_valid() == validity
    assert type(form.cleaned_data['notes']) == list
    assert form.cleaned_data['notes'] == str(notes).split('\r\n')

