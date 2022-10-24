from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import RawRod


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Login: ')
    password = forms.CharField(label='Password: ', widget=forms.PasswordInput(attrs={'class': 'required'}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Login: ')
    password1 = forms.CharField(label='Password: ', widget=forms.PasswordInput(attrs={'class': 'required'}))
    password2 = forms.CharField(label='Repeat password: ', widget=forms.PasswordInput(attrs={'class': 'required'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CreateRawRodForm(forms.ModelForm):
    notes = forms.CharField(required=False, label='Notes', widget=forms.Textarea())

    class Meta:
        model = RawRod
        exclude = ['rod_id', 'number', 'created_by', 'updated_by']
        widgets = {
            'material': forms.Select(),
            'length': forms.NumberInput(),
        }

    def get_initial_for_field(self, field, field_name):
        if field_name == 'notes':
            try:
                notes = self.instance.rawrodnote_set.select_related('rod').all()
                return '\n'.join([note.note for note in notes])
            except Exception as ex:
                print(ex)

        return super().get_initial_for_field(field, field_name)

    def clean_notes(self):
        return [note for note in self.cleaned_data.get('notes').split('\r\n')]
