from django.db.models import Prefetch
from django.shortcuts import redirect
from django.views import generic

from .forms import CreateRodPieceForm
from .models import RodPiece, RodPieceNote


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


class CreateRodPiece(generic.CreateView):
    form_class = CreateRodPieceForm
    template_name = 'create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rod_name'] = self.kwargs.get('rod_name')
        return context

    def form_valid(self, form):
        rod = RodPiece.objects.create(
            material=self.request.POST.get('material'),
            analysis_technique=form.cleaned_data.get('analysis_technique'),
            sample_state=form.cleaned_data.get('sample_state'),
            created_by=self.request.user,
        )

        [RodPieceNote.objects.create(text=note, rod=rod) for note in form.cleaned_data.get('notes')]

        return redirect('rod_pieces:table', self.request.POST.get('material'))
