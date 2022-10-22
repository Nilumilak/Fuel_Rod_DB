from django.db.models import Prefetch
from django.views import generic
from .models import RawRod


class ShowTable(generic.ListView):
    queryset = RawRod.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('rawrodnote_set')).all()
    context_object_name = 'rods'
    template_name = 'fresh_inventory/table.html'