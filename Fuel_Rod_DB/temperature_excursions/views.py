from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateRodTemperatureTestForm
from .models import RodTemperatureTest, RodTemperatureTestNote


class ShowTable(generic.DetailView):
    template_name = 'temperature_excursions/table.html'

    def get_object(self, queryset=None):
        return None

    def get_context_data(self, **kwargs):
        material = self.kwargs.get('rod_name')
        queryset = RodTemperatureTest.objects.select_related('created_by', 'updated_by').prefetch_related(
            Prefetch('rodtemperaturetestnote_set')).filter(exp_id=material)
        context = {'rod_name': material, 'rods': queryset}
        return context


class CreateRodTemperatureTest(LoginRequiredMixin, generic.CreateView):
    form_class = CreateRodTemperatureTestForm
    template_name = 'create.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rod_name'] = self.kwargs.get('rod_name')
        return context

    def form_valid(self, form):
        rod = RodTemperatureTest.objects.create(
            exp_id=self.request.POST.get('material'),
            original_length=form.cleaned_data.get('original_length'),
            power=form.cleaned_data.get('power'),
            max_temperature=form.cleaned_data.get('max_temperature'),
            heating_time=form.cleaned_data.get('heating_time'),
            created_by=self.request.user,
            updated_by=self.request.user,
        )

        [RodTemperatureTestNote.objects.create(text=note, rod=rod) for note in form.cleaned_data.get('notes')]
        print(self.request.POST)

        return redirect('temperature_excursions:table', self.request.POST.get('material'))
