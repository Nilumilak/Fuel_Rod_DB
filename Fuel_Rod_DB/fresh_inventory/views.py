from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import CreateView

from .forms import LoginUserForm, RegisterUserForm, CreateRawRodForm
from .models import RawRod, RawRodNote


class ShowTable(generic.ListView):
    queryset = RawRod.objects.select_related('material', 'created_by', 'updated_by').prefetch_related(Prefetch('rawrodnote_set')).all()
    context_object_name = 'rods'
    template_name = 'fresh_inventory/table.html'


class CreateRawRod(generic.CreateView):
    form_class = CreateRawRodForm
    template_name = 'create.html'

    def form_valid(self, form):
        rod = RawRod.objects.create(
            material=form.cleaned_data.get('material'),
            length=form.cleaned_data.get('length'),
            created_by=self.request.user,
        )

        [RawRodNote.objects.create(text=note, rod=rod) for note in form.cleaned_data.get('notes')]

        return redirect('fresh_inventory:table')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'fresh_inventory/login.html'

    def get_success_url(self):
        return reverse('fresh_inventory:table')


class RegistrationUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'fresh_inventory/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('fresh_inventory:table')


def logout_user(request):
    logout(request)
    return redirect('fresh_inventory:table')