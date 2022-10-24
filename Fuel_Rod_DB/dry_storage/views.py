from django.db.models import Prefetch
from django.shortcuts import redirect
from django.views import generic

from .forms import CreateRodDryStorageTestForm
from .models import RodDryStorageTest, RodDryStorageTestNote


class ShowTable(generic.ListView):
    queryset = RodDryStorageTest.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('roddrystoragetestnote_set')).all()
    context_object_name = 'rods'
    template_name = 'dry_storage/table.html'


class CreateRodDryStorageTest(generic.CreateView):
    form_class = CreateRodDryStorageTestForm
    template_name = 'create.html'

    def form_valid(self, form):
        rod = RodDryStorageTest.objects.create(
            material=form.cleaned_data.get('material'),
            original_length=form.cleaned_data.get('original_length'),
            heating_rate=form.cleaned_data.get('heating_rate'),
            cooling_rate=form.cleaned_data.get('cooling_rate'),
            max_temperature=form.cleaned_data.get('max_temperature'),
            heating_time=form.cleaned_data.get('heating_time'),
            cooling_time=form.cleaned_data.get('cooling_time'),
            created_by=self.request.user,
        )

        [RodDryStorageTestNote.objects.create(text=note, rod=rod) for note in form.cleaned_data.get('notes')]

        return redirect('dry_storage:table')