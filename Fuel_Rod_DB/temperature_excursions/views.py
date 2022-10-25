from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateRodTemperatureTestForm
from .models import RodTemperatureTest, RodTemperatureTestNote


class ShowTable(generic.ListView):
    queryset = RodTemperatureTest.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('rodtemperaturetestnote_set')).all()
    context_object_name = 'rods'
    template_name = 'temperature_excursions/table.html'


class CreateRodTemperatureTest(LoginRequiredMixin, generic.CreateView):
    form_class = CreateRodTemperatureTestForm
    template_name = 'create.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def form_valid(self, form):
        rod = RodTemperatureTest.objects.create(
            material=form.cleaned_data.get('material'),
            original_length=form.cleaned_data.get('original_length'),
            power=form.cleaned_data.get('power'),
            max_temperature=form.cleaned_data.get('max_temperature'),
            heating_time=form.cleaned_data.get('heating_time'),
            quenched=form.cleaned_data.get('quenched'),
            created_by=self.request.user,
            updated_by=self.request.user,
        )

        [RodTemperatureTestNote.objects.create(text=note, rod=rod) for note in form.cleaned_data.get('notes')]

        return redirect('temperature_excursions:table')
