import pytest

from dry_storage_exp.forms import CreateDryStorageExpForm
from fresh_inventory.models import RawRod


fixture = [
    ('test_note', True),
    ('test_note_1\r\ntest_note_2', True),
    (123, True),
    ('', True),
]


@pytest.mark.django_db
@pytest.mark.parametrize('notes, validity', fixture)
def test_form(notes, validity, rod_factory):
    material = rod_factory()
    form = CreateDryStorageExpForm(data={
        'material': material,
        'notes': notes
    })
    form.save()
    assert form.is_valid() == validity
    assert type(form.cleaned_data['material']) == RawRod
    assert type(form.cleaned_data['notes']) == list
    assert form.cleaned_data['notes'] == str(notes).split('\r\n')
