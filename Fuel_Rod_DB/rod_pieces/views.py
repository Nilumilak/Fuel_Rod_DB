from django.db.models import Prefetch
from django.views import generic

from .models import RodPiece


class ShowTable(generic.DetailView):
    template_name = 'rod_pieces/table.html'

    def get_object(self, queryset=None):
        return None

    def get_context_data(self, **kwargs):
        material = self.kwargs.get('rod_name')
        queryset = RodPiece.objects.select_related('analysis_technique', 'sample_state', 'created_by',
                                                   'updated_by').prefetch_related(Prefetch('rodpiecenote_set')).filter(material=material)
        context = {'rod_name': material, 'rods': queryset}
        return context