from django.urls import path
from .views import ShowTable, CreateRodTemperatureTest

app_name = 'temperature_excursions'

urlpatterns = [
    path('<slug:rod_name>', ShowTable.as_view(), name='table'),
    path('<slug:rod_name>/create_rod_temperature_test/', CreateRodTemperatureTest.as_view(), name='create'),
]