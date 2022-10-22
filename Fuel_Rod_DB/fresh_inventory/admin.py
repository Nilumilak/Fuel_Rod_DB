from django.contrib import admin

from .models import RawRod, Material, RawRodNote


@admin.register(RawRodNote)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Material)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(RawRod)
class StudentAdmin(admin.ModelAdmin):
    fields = ['material', 'length', 'created_by', 'updated_by']
    list_display = ['rod_id', 'length', 'created_at', 'updated_at', 'created_by', 'updated_by']
    list_editable = ['length']
