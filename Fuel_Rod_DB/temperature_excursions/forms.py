from django import forms
from .models import RodTemperatureTest


class CreateRodTemperatureTestForm(forms.ModelForm):
    notes = forms.CharField(required=False, label='Notes', widget=forms.Textarea())

    class Meta:
        model = RodTemperatureTest
        exclude = ['rod_id', 'number', 'raw_rod', 'created_by', 'updated_by']
        widgets = {
            'original_length': forms.NumberInput(),
            'power': forms.NumberInput(),
            'max_temperature': forms.NumberInput(),
            'heating_time': forms.NumberInput(),
        }

    def get_initial_for_field(self, field, field_name):
        if field_name == 'notes':
            try:
                notes = self.instance.rodtemperaturetestnote_set.select_related('rod').all()
                return '\n'.join([note.note for note in notes])
            except Exception as ex:
                print(ex)

        return super().get_initial_for_field(field, field_name)

    def clean_notes(self):
        return [note for note in self.cleaned_data.get('notes').split('\r\n')]
