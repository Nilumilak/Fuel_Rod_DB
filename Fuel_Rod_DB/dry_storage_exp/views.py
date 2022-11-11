from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CreateDryStorageExpForm, UpdateDryStorageExpForm
from .models import DryStorageExp, DryStorageExpNote


SORT_MAP = {'exp_id': 'exp_id', '-exp_id': '-exp_id',
            'material': 'material__name', '-material': '-material__name',
            'created_at': 'created_at', '-created_at': '-created_at',
            'updated_at': 'updated_at', '-updated_at': '-updated_at'}


class ShowTable(generic.ListView):
    queryset = DryStorageExp.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('drystorageexpnote_set')).all()
    context_object_name = 'rods'
    template_name = 'dry_storage_exp/table.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'q' in self.request.GET:
            context['sort_key'] = self.request.GET['q']
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

        DryStorageExpNote.objects.bulk_create([DryStorageExpNote(text=text, rod=rod) for text in form.cleaned_data.get('notes')])

        return redirect('dry_storage_exp:table')


class UpdateDryStorageExp(LoginRequiredMixin, generic.UpdateView):
    model = DryStorageExp
    form_class = UpdateDryStorageExpForm
    template_name = 'update.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def get_object(self, queryset=None):
        return DryStorageExp.objects.get(exp_id=self.kwargs.get('rod_name'))

    def form_valid(self, form):
        DryStorageExpNote.objects.filter(rod=self.object).delete()
        DryStorageExpNote.objects.bulk_create([DryStorageExpNote(text=text, rod=self.object) for text in form.cleaned_data.get('notes')])
        self.object.updated_by = self.request.user
        self.object.save()
        return redirect('dry_storage_exp:table')


def delete_rod(request, pk):
    DryStorageExp.objects.get(id=pk).delete()
    return redirect('dry_storage_exp:table')
