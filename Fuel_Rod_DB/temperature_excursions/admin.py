from django.contrib import admin

from .models import RodTemperatureTest, RodTemperatureTestNote


@admin.register(RodTemperatureTest)
class RodTemperatureTestAdmin(admin.ModelAdmin):
    fields = ['material', 'original_length', 'power', 'max_temperature',
              'heating_time', 'quenched', 'created_by', 'updated_by']
    list_display = ['rod_id', 'material', 'original_length',
                    'power', 'max_temperature', 'heating_time', 'quenched',
                    'created_by', 'updated_by']
    list_editable = ['original_length', 'power', 'max_temperature', 'heating_time', 'quenched']


@admin.register(RodTemperatureTestNote)
class RodTemperatureTestNoteAdmin(admin.ModelAdmin):
    pass
