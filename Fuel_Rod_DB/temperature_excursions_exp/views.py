from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateTemperatureExcursionExpForm
from .models import TemperatureExcursionExp, TemperatureExcursionExpNote


class ShowTable(generic.ListView):
    queryset = TemperatureExcursionExp.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('temperatureexcursionexpnote_set')).all()
    context_object_name = 'rods'
    template_name = 'temperature_excursions_exp/table.html'


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

        [TemperatureExcursionExpNote.objects.create(text=note, rod=rod) for note in form.cleaned_data.get('notes')]

        return redirect('temperature_excursions_exp:table')
