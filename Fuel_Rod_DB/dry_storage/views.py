from django.db.models import Prefetch
from django.views import generic

from .models import RodDryStorageTest


class ShowTable(generic.ListView):
    queryset = RodDryStorageTest.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('roddrystoragetestnote_set')).all()
    context_object_name = 'rods'
    template_name = 'dry_storage/table.html'