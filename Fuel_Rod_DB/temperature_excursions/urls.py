from django.urls import path
from .views import ShowTable, CreateRodTemperatureTest

app_name = 'temperature_excursions'

urlpatterns = [
    path('', ShowTable.as_view(), name='table'),
    path('create_rod_temperature_test/', CreateRodTemperatureTest.as_view(), name='create'),
]