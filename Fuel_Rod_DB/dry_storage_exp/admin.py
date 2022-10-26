from django.contrib import admin

from .models import DryStorageExp, DryStorageExpNote


@admin.register(DryStorageExp)
class DryStorageExpAdmin(admin.ModelAdmin):
    fields = ['material', 'created_by', 'updated_by']
    list_display = ['exp_id', 'material', 'created_by', 'updated_by']


@admin.register(DryStorageExpNote)
class DryStorageExpNoteAdmin(admin.ModelAdmin):
    pass
