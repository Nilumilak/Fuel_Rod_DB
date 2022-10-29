from django.contrib import admin

from .models import RodDryStorageTest, RodDryStorageTestNote


@admin.register(RodDryStorageTest)
class RodDryStorageTestAdmin(admin.ModelAdmin):
    fields = ['raw_rod', 'original_length', 'heating_rate', 'cooling_rate',
              'max_temperature', 'heating_time', 'cooling_time', 'created_by', 'updated_by']
    list_display = ['rod_id', 'raw_rod', 'original_length', 'heating_rate',
                    'cooling_rate', 'max_temperature', 'heating_time', 'cooling_time',
                    'created_by', 'updated_by']
    list_editable = ['original_length', 'heating_rate', 'cooling_rate',
                     'max_temperature', 'heating_time', 'cooling_time']


@admin.register(RodDryStorageTestNote)
class RodDryStorageTestNoteAdmin(admin.ModelAdmin):
    pass
