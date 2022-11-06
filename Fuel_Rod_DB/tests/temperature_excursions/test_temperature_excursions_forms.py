import pytest

from temperature_excursions.forms import CreateRodTemperatureTestForm

fixture = [
    #  all correct
    (5, 5, 5, 5, 'test_note', True),
    # all correct
    ('5', '5', '5', '5', 'test_note', True),
    # all fields should be filled out
    (5, '', 5, 5, 'test_note', False),
    # only digits are allowed for the field
    (5, 'qwe', 5, 5, 'test_note', False),
    # more than one note
    (5, 5, 5, 5, 'test_note\r\ntest_note', True),
]


@pytest.mark.parametrize('original_length, power, max_temperature, heating_time, notes, validity', fixture)
def test_form(original_length, power, max_temperature, heating_time, notes, validity):
    """
    CreateRodTemperatureTestForm test
    """
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

