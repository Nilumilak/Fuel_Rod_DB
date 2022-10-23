from django.urls import path
from .views import ShowTable

app_name = 'temperature_excursions'

urlpatterns = [
    path('/', ShowTable.as_view(), name='table'),
]