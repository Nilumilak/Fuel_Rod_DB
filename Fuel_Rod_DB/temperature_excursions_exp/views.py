from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateTemperatureExcursionExpForm, UpdateTemperatureExcursionExpForm
from .models import TemperatureExcursionExp, TemperatureExcursionExpNote


SORT_MAP = {'exp_id': 'exp_id', '-exp_id': '-exp_id',
            'material': 'material__name', '-material': '-material__name',
            'created_at': 'created_at', '-created_at': '-created_at',
            'updated_at': 'updated_at', '-updated_at': '-updated_at'}


class ShowTable(generic.ListView):
    queryset = TemperatureExcursionExp.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('temperatureexcursionexpnote_set')).all()
    context_object_name = 'rods'
    template_name = 'temperature_excursions_exp/table.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'q' in self.request.GET:
            context['sort_key'] = self.request.GET['q']
            context['rods'] = context['rods'].order_by(SORT_MAP[self.request.GET['q']])
        return context


class CreateTemperatureExcursionExp(LoginRequiredMixin, generic.CreateView):
    form_class = CreateTemperatureExcursionExpForm
    template_name = 'create.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def form_valid(self, form):
        rod = TemperatureExcursionExp.objects.create(
            material=form.cleaned_data.get('material'),
            quenched=form.cleaned_data.get('quenched'),
            created_by=self.request.user,
            updated_by=self.request.user,
        )

        TemperatureExcursionExpNote.objects.bulk_create([TemperatureExcursionExpNote(text=text, rod=rod) for text in form.cleaned_data.get('notes')])

        return redirect('temperature_excursions_exp:table')


class UpdateTemperatureExcursionExp(LoginRequiredMixin, generic.UpdateView):
    model = TemperatureExcursionExp
    form_class = UpdateTemperatureExcursionExpForm
    template_name = 'update.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def get_object(self, queryset=None):
        return TemperatureExcursionExp.objects.get(exp_id=self.kwargs.get('rod_name'))

    def form_valid(self, form):
        TemperatureExcursionExpNote.objects.filter(rod=self.object).delete()
        TemperatureExcursionExpNote.objects.bulk_create([TemperatureExcursionExpNote(text=text, rod=self.object) for text in form.cleaned_data.get('notes')])
        self.object.updated_by = self.request.user
        self.object.save()
        return redirect('temperature_excursions_exp:table')


@login_required
def delete_rod(request, pk):
    TemperatureExcursionExp.objects.get(id=pk).delete()
    return redirect('temperature_excursions_exp:table')
