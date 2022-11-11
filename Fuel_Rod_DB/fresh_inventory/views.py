from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch, Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

from .forms import LoginUserForm, RegisterUserForm, CreateRawRodForm, UpdateRawRodForm
from .models import RawRod, RawRodNote


SORT_MAP = {'rod_id': 'rod_id', '-rod_id': '-rod_id',
            'material': 'material__name', '-material': '-material__name',
            'length': 'length', '-length': '-length',
            'created_at': 'created_at', '-created_at': '-created_at',
            'updated_at': 'updated_at', '-updated_at': '-updated_at'}


class ShowTable(generic.ListView):
    queryset = RawRod.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('rawrodnote_set')).all()
    context_object_name = 'rods'
    template_name = 'fresh_inventory/table.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'q' in self.request.GET:
            context['sort_key'] = self.request.GET['q']
            context['rods'] = context['rods'].order_by(SORT_MAP[self.request.GET['q']])
        return context


class CreateRawRod(LoginRequiredMixin, generic.CreateView):
    form_class = CreateRawRodForm
    template_name = 'create.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def form_valid(self, form):
        rod = RawRod.objects.create(
            material=form.cleaned_data.get('material'),
            length=form.cleaned_data.get('length'),
            created_by=self.request.user,
            updated_by=self.request.user,
        )

        RawRodNote.objects.bulk_create([RawRodNote(text=text, rod=rod) for text in form.cleaned_data.get('notes')])

        return redirect('fresh_inventory:table')


class UpdateRawRod(LoginRequiredMixin, generic.UpdateView):
    model = RawRod
    form_class = UpdateRawRodForm
    template_name = 'update.html'
    login_url = reverse_lazy('fresh_inventory:login')

    def get_object(self, queryset=None):
        return RawRod.objects.get(rod_id=self.kwargs.get('rod_name'))

    def form_valid(self, form):
        RawRodNote.objects.filter(rod=self.object).delete()
        RawRodNote.objects.bulk_create([RawRodNote(text=text, rod=self.object) for text in form.cleaned_data.get('notes')])
        self.object.updated_by = self.request.user
        self.object.save()
        return redirect('fresh_inventory:table')


def delete_rod(request, rod_name):
    RawRod.objects.get(rod_id=rod_name).delete()
    return redirect('fresh_inventory:table')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'fresh_inventory/login.html'

    def get_success_url(self):
        return reverse('fresh_inventory:table')


class RegistrationUser(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'fresh_inventory/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('fresh_inventory:table')


def logout_user(request):
    logout(request)
    return redirect('fresh_inventory:table')