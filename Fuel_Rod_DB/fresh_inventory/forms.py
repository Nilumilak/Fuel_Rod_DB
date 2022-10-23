from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login: ')
    password = forms.CharField(label='Password: ')


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login: ')
    password1 = forms.CharField(label='Password: ')
    password2 = forms.CharField(label='Repeat password: ')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']