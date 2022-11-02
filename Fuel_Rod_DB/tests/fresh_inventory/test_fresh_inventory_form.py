import pytest

from fresh_inventory.forms import CreateRawRodForm, LoginUserForm, RegisterUserForm
from fresh_inventory.models import Material

fixture = [
    (100, 'test_note', True),
    ('100', 'test_note_1\r\ntest_note_2', True),
    (100, 123, True),
    (100, '', True),
    ('test', 'test_note', False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('length, notes, validity', fixture)
def test_create_form(length, notes, validity, material_factory):
    material = material_factory()
    form = CreateRawRodForm(data={
        'material': material,
        'length': length,
        'notes': notes
    })
    assert form.is_valid() == validity
    assert type(form.cleaned_data['material']) == Material
    assert type(form.cleaned_data['notes']) == list
    assert form.cleaned_data['notes'] == str(notes).split('\r\n')


fixture = [
    ('user', 'user', True),
    ('admin', 'admin', False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('username, password, validity', fixture)
def test_login_user(username, password, validity, user):
    form = LoginUserForm(data={
        'username': username,
        'password': password,
    })

    assert form.is_valid() == validity


fixture = [
    ('test_user', 'testpassword123', 'testpassword123', True),
    ('admin', 'testpassword123', 'testpassword123', True),
    ('user', 'testpassword123', 'testpassword123', False),
    ('test_user', 'test', 'test', False),
    ('test_user', 'test_user', 'test_user', False),
    (111, 111, 111, False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('username, password1, password2, validity', fixture)
def test_register_user(username, password1, password2, validity, user):
    form = RegisterUserForm(data={
        'username': username,
        'password1': password1,
        'password2': password2,
    })

    assert form.is_valid() == validity
