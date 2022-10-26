from django import forms
from .models import TemperatureExcursionExp


class CreateTemperatureExcursionExpForm(forms.ModelForm):
    notes = forms.CharField(required=False, label='Notes', widget=forms.Textarea())

    class Meta:
        model = TemperatureExcursionExp
        exclude = ['exp_id', 'number', 'created_by', 'updated_by']
        widgets = {
            'material': forms.Select(),
            'quenched': forms.CheckboxInput(),
        }

    def get_initial_for_field(self, field, field_name):
        if field_name == 'notes':
            try:
                notes = self.instance.temperatureexcursionexpnote_set.select_related('rod').all()
                return '\n'.join([note.note for note in notes])
            except Exception as ex:
                print(ex)

        return super().get_initial_for_field(field, field_name)

    def clean_notes(self):
        return [note for note in self.cleaned_data.get('notes').split('\r\n')]
