from django.contrib import admin

from temperature_excursions_exp.models import TemperatureExcursionExp, TemperatureExcursionExpNote


@admin.register(TemperatureExcursionExp)
class TemperatureExcursionExpAdmin(admin.ModelAdmin):
    fields = ['material', 'quenched', 'created_by', 'updated_by']
    list_display = ['exp_id', 'material', 'quenched',
                    'created_by', 'updated_by']
    list_editable = ['quenched']


@admin.register(TemperatureExcursionExpNote)
class TemperatureExcursionExpNoteAdmin(admin.ModelAdmin):
    pass