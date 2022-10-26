from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateRodDryStorageTestForm
from .models import RodDryStorageTest, RodDryStorageTestNote


class ShowTable(generic.DetailView):
    template_name = 'dry_storage/table.html'

    def get_object(self, queryset=None):
        return None

    def get_context_data(self, **kwargs):
        material = self.kwargs.get('rod_name')
        queryset = RodDryStorageTest.objects.select_related('created_by', 'updated_by').prefetch_related(
            Prefetch('roddrystoragetestnote_set')).filter(exp_id=material)
        context = {'rod_name': material, 'rods': queryset}
        return context


class CreateRodDryStorageTest(LoginRequiredMixin, generic.CreateView):
    form_class = CreateRodDryStorageTestForm
    template_name = 'create.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rod_name'] = self.kwargs.get('rod_name')
        return context

    def form_valid(self, form):
        rod = RodDryStorageTest.objects.create(
            exp_id=self.request.POST.get('material'),
            original_length=form.cleaned_data.get('original_length'),
            heating_rate=form.cleaned_data.get('heating_rate'),
            cooling_rate=form.cleaned_data.get('cooling_rate'),
            max_temperature=form.cleaned_data.get('max_temperature'),
            heating_time=form.cleaned_data.get('heating_time'),
            cooling_time=form.cleaned_data.get('cooling_time'),
            created_by=self.request.user,
            updated_by=self.request.user,
        )

        [RodDryStorageTestNote.objects.create(text=note, rod=rod) for note in form.cleaned_data.get('notes')]

        return redirect('dry_storage:table', self.request.POST.get('material'))
