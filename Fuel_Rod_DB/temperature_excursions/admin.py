from django.contrib import admin

from .models import RodTemperatureTest, RodTemperatureTestNote


@admin.register(RodTemperatureTest)
class RodTemperatureTestAdmin(admin.ModelAdmin):
    fields = ['exp_id', 'original_length', 'power', 'max_temperature',
              'heating_time', 'created_by', 'updated_by']
    list_display = ['rod_id', 'exp_id', 'original_length',
                    'power', 'max_temperature', 'heating_time',
                    'created_by', 'updated_by']
    list_editable = ['original_length', 'power', 'max_temperature', 'heating_time']


@admin.register(RodTemperatureTestNote)
class RodTemperatureTestNoteAdmin(admin.ModelAdmin):
    pass
