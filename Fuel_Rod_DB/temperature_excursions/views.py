from django.db.models import Prefetch
from django.views import generic

from .models import RodTemperatureTest


class ShowTable(generic.ListView):
    queryset = RodTemperatureTest.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('rodtemperaturetestnote_set')).all()
    context_object_name = 'rods'
    template_name = 'temperature_excursions/table.html'