import pytest

from fresh_inventory.forms import CreateRawRodForm, LoginUserForm, RegisterUserForm
from fresh_inventory.models import Material

fixture = [
    #  all correct
    (100, 'test_note', True),
    #  more than one note
    ('100', 'test_note_1\r\ntest_note_2', True),
    #  all correct
    (100, 123, True),
    #  notes are not required
    (100, '', True),
    # only digits are allowed for the field
    ('test', 'test_note', False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('length, notes, validity', fixture)
def test_create_form(length, notes, validity, material_factory):
    """
    CreateRawRodForm test
    """
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
    # user exists
    ('user', 'user', True),
    # user does not exist
    ('test_user', 'test_user', False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('username, password, validity', fixture)
def test_login_user(username, password, validity, user):
    """
    LoginUserForm test
    """
    form = LoginUserForm(data={
        'username': username,
        'password': password,
    })

    assert form.is_valid() == validity


fixture = [
    # all correct
    ('test_user', 'testpassword123', 'testpassword123', True),
    # user with this name already exists
    ('user', 'testpassword123', 'testpassword123', False),
    # password too short
    ('test_user', 'test', 'test', False),
    # password contain username
    ('test_user123', 'test_user123', 'test_user123', False),
]


@pytest.mark.django_db
@pytest.mark.parametrize('username, password1, password2, validity', fixture)
def test_register_user(username, password1, password2, validity, user):
    """
    RegisterUserForm test
    """
    form = RegisterUserForm(data={
        'username': username,
        'password1': password1,
        'password2': password2,
    })

    assert form.is_valid() == validity
