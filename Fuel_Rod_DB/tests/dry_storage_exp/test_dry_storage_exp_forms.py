import pytest

from dry_storage_exp.forms import CreateDryStorageExpForm, UpdateDryStorageExpForm
from fresh_inventory.models import RawRod


fixture = [
    # all correct
    ('test_note', True),
    # more than one note
    ('test_note_1\r\ntest_note_2', True),
    # all correct
    (123, True),
    # notes are not required
    ('', True),
]


@pytest.mark.django_db
@pytest.mark.parametrize('notes, validity', fixture)
def test_create_form(notes, validity, rod_factory):
    """
    CreateDryStorageExpForm test
    """
    material = rod_factory()
    form = CreateDryStorageExpForm(data={
        'material': material,
        'notes': notes
    })
    assert form.is_valid() == validity
    assert type(form.cleaned_data['material']) == RawRod
    assert type(form.cleaned_data['notes']) == list
    assert form.cleaned_data['notes'] == str(notes).split('\r\n')


fixture = [
    # all correct
    ('test_note', True),
    # more than one note
    ('test_note_1\r\ntest_note_2', True),
    # all correct
    (123, True),
    # notes are not required
    ('', True),
]


@pytest.mark.django_db
@pytest.mark.parametrize('notes, validity', fixture)
def test_update_form(notes, validity, rod_factory):
    """
    UpdateDryStorageExpForm test
    """
    form = UpdateDryStorageExpForm(data={
        'notes': notes
    })
    assert form.is_valid() == validity
    assert type(form.cleaned_data['notes']) == list
    assert form.cleaned_data['notes'] == str(notes).split('\r\n')
