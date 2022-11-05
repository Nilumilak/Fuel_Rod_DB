from django import forms
from .models import RodDryStorageTest


class CreateRodDryStorageTestForm(forms.ModelForm):
    notes = forms.CharField(required=False, label='Notes', widget=forms.Textarea())

    class Meta:
        model = RodDryStorageTest
        exclude = ['rod_id', 'number', 'raw_rod', 'created_by', 'updated_by']
        widgets = {
            'original_length': forms.NumberInput(),
            'heating_rate': forms.NumberInput(),
            'cooling_rate': forms.NumberInput(),
            'max_temperature': forms.NumberInput(),
            'heating_time': forms.NumberInput(),
            'cooling_time': forms.NumberInput(),
        }

    def get_initial_for_field(self, field, field_name):
        if field_name == 'notes':
            try:
                notes = self.instance.roddrystoragetestnote_set.select_related('rod').all()
                return '\n'.join([note.text for note in notes])
            except Exception as ex:
                print(ex)

        return super().get_initial_for_field(field, field_name)

    def clean_notes(self):
        return [note for note in self.cleaned_data.get('notes').split('\r\n')]
