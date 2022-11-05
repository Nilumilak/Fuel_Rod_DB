from django import forms
from .models import RodPiece


class CreateRodPieceForm(forms.ModelForm):
    notes = forms.CharField(required=False, label='Notes', widget=forms.Textarea())

    class Meta:
        model = RodPiece
        exclude = ['rod_id', 'material', 'number', 'created_by', 'updated_by']
        widgets = {
            'analysis_technique': forms.Select(),
            'sample_state': forms.Select(),
        }

    def get_initial_for_field(self, field, field_name):
        if field_name == 'notes':
            try:
                notes = self.instance.rodpiecenote_set.select_related('rod').all()
                return '\n'.join([note.text for note in notes])
            except Exception as ex:
                print(ex)

        return super().get_initial_for_field(field, field_name)

    def clean_notes(self):
        return [note for note in self.cleaned_data.get('notes').split('\r\n')]
