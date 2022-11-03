from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateDryStorageExpForm
from .models import DryStorageExp, DryStorageExpNote


SORT_MAP = {'exp_id': 'exp_id', 'material': 'material__name', 'created_at': 'created_at', 'updated_at': 'updated_at'}


class ShowTable(generic.ListView):
    queryset = DryStorageExp.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('drystorageexpnote_set')).all()
    context_object_name = 'rods'
    template_name = 'dry_storage_exp/table.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'q' in self.request.GET:
            context['rods'] = context['rods'].order_by(SORT_MAP[self.request.GET['q']])
        return context


class CreateDryStorageExp(LoginRequiredMixin, generic.CreateView):
    form_class = CreateDryStorageExpForm
    template_name = 'create.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def form_valid(self, form):
        rod = DryStorageExp.objects.create(
            material=form.cleaned_data.get('material'),
            created_by=self.request.user,
            updated_by=self.request.user,
        )

        [DryStorageExpNote.objects.create(text=note, rod=rod) for note in form.cleaned_data.get('notes')]

        return redirect('dry_storage_exp:table')
