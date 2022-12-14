from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateRodPieceForm, UpdateRodPieceForm
from .models import RodPiece, RodPieceNote


SORT_MAP = {'rod_id': 'rod_id', '-rod_id': '-rod_id',
            'analysis_technique': 'analysis_technique', '-analysis_technique': '-analysis_technique',
            'sample_state': 'sample_state', '-sample_state': '-sample_state',
            'created_at': 'created_at', '-created_at': '-created_at',
            'updated_at': 'updated_at', '-updated_at': '-updated_at'}


class ShowTable(generic.DetailView):
    template_name = 'rod_pieces/table.html'

    def get_object(self, queryset=None):
        return None

    def get_context_data(self, **kwargs):
        material = self.kwargs.get('rod_name')
        queryset = RodPiece.objects.select_related('analysis_technique', 'sample_state', 'created_by',
                                                   'updated_by').prefetch_related(Prefetch('rodpiecenote_set')).filter(material=material)
        context = {'rod_name': material, 'rods': queryset}
        if 'q' in self.request.GET:
            context['sort_key'] = self.request.GET['q']
            context['rods'] = context['rods'].order_by(SORT_MAP[self.request.GET['q']])
        return context


class CreateRodPiece(LoginRequiredMixin, generic.CreateView):
    form_class = CreateRodPieceForm
    template_name = 'create.html'
    login_url = reverse_lazy('fresh_inventory:login')

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
            updated_by=self.request.user,
        )

        RodPieceNote.objects.bulk_create([RodPieceNote(text=text, rod=rod) for text in form.cleaned_data.get('notes')])

        return redirect('rod_pieces:table', self.request.POST.get('material'))


class UpdateRodPiece(LoginRequiredMixin, generic.UpdateView):
    model = RodPiece
    form_class = UpdateRodPieceForm
    template_name = 'update.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def get_object(self, queryset=None):
        return RodPiece.objects.get(rod_id=self.kwargs.get('rod_name'))

    def form_valid(self, form):
        RodPieceNote.objects.filter(rod=self.object).delete()
        RodPieceNote.objects.bulk_create([RodPieceNote(text=text, rod=self.object) for text in form.cleaned_data.get('notes')])
        self.object.updated_by = self.request.user
        self.object.save()
        return redirect('rod_pieces:table', self.object.material)


@login_required
def delete_rod(request, pk):
    rod = RodPiece.objects.get(id=pk)
    rod.delete()
    return redirect('rod_pieces:table', rod.material)
