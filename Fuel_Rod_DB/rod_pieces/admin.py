from django.contrib import admin

from rod_pieces.models import RodPieceNote, AnalysisTechnique, SampleState, RodPiece


@admin.register(RodPieceNote)
class RodPieceNoteAdmin(admin.ModelAdmin):
    pass


@admin.register(AnalysisTechnique)
class AnalysisTechniqueAdmin(admin.ModelAdmin):
    pass


@admin.register(SampleState)
class SampleStateAdmin(admin.ModelAdmin):
    pass


@admin.register(RodPiece)
class RodPieceAdmin(admin.ModelAdmin):
    list_display = ['rod_id', 'analysis_technique', 'sample_state', 'created_by', 'updated_by']
    fields = ['material', 'analysis_technique', 'sample_state', 'created_by', 'updated_by']
    list_editable = ['sample_state', 'created_by', 'updated_by']