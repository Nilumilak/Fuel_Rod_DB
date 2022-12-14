from django.urls import path
from .views import ShowTable, CreateTemperatureExcursionExp, UpdateTemperatureExcursionExp, delete_rod

app_name = 'temperature_excursions_exp'

urlpatterns = [
    path('', ShowTable.as_view(), name='table'),
    path('create_temperature_excursion_exp/', CreateTemperatureExcursionExp.as_view(), name='create'),
    path('update_temperature_excursion_exp/<slug:rod_name>/', UpdateTemperatureExcursionExp.as_view(), name='update'),
    path('delete_temperature_excursion_exp/<int:pk>/', delete_rod, name='delete'),
]
