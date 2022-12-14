from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from temperature_excursions_exp.models import TemperatureExcursionExp
from .forms import CreateRodTemperatureTestForm, UpdateRodTemperatureTestForm
from .models import RodTemperatureTest, RodTemperatureTestNote


SORT_MAP = {'rod_id': 'rod_id', '-rod_id': '-rod_id',
            'original_length': 'original_length', '-original_length': '-original_length',
            'power': 'power', '-power': '-power',
            'max_temperature': 'max_temperature', '-max_temperature': '-max_temperature',
            'heating_time': 'heating_time', '-heating_time': '-heating_time',
            'created_at': 'created_at', '-created_at': '-created_at',
            'updated_at': 'updated_at', '-updated_at': '-updated_at'}


class ShowTable(generic.DetailView):
    template_name = 'temperature_excursions/table.html'

    def get_object(self, queryset=None):
        return None

    def get_context_data(self, **kwargs):
        material = self.kwargs.get('rod_name')
        queryset = RodTemperatureTest.objects.select_related('created_by', 'updated_by').prefetch_related(
            Prefetch('rodtemperaturetestnote_set')).filter(raw_rod__exp_id=material)
        context = {'rod_name': material, 'rods': queryset}
        if 'q' in self.request.GET:
            context['sort_key'] = self.request.GET['q']
            context['rods'] = context['rods'].order_by(SORT_MAP[self.request.GET['q']])
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
        exp_id = self.request.POST.get('material')

        raw_rod = TemperatureExcursionExp.objects.get(exp_id=exp_id)

        rod = RodTemperatureTest.objects.create(
            raw_rod=raw_rod,
            original_length=form.cleaned_data.get('original_length'),
            power=form.cleaned_data.get('power'),
            max_temperature=form.cleaned_data.get('max_temperature'),
            heating_time=form.cleaned_data.get('heating_time'),
            created_by=self.request.user,
            updated_by=self.request.user,
        )

        RodTemperatureTestNote.objects.bulk_create([RodTemperatureTestNote(text=text, rod=rod) for text in form.cleaned_data.get('notes')])

        return redirect('temperature_excursions:table', self.request.POST.get('material'))


class UpdateRodTemperatureTest(LoginRequiredMixin, generic.UpdateView):
    model = RodTemperatureTest
    form_class = UpdateRodTemperatureTestForm
    template_name = 'update.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def get_object(self, queryset=None):
        return RodTemperatureTest.objects.get(rod_id=self.kwargs.get('rod_name'))

    def form_valid(self, form):
        RodTemperatureTestNote.objects.filter(rod=self.object).delete()
        RodTemperatureTestNote.objects.bulk_create([RodTemperatureTestNote(text=text, rod=self.object) for text in form.cleaned_data.get('notes')])
        self.object.updated_by = self.request.user
        self.object.save()
        return redirect('temperature_excursions:table', self.object.raw_rod)


@login_required
def delete_rod(request, pk):
    rod = RodTemperatureTest.objects.get(id=pk)
    rod.delete()
    return redirect('temperature_excursions:table', rod.raw_rod)

