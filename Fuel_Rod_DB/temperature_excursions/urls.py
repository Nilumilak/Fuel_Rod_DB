from django.urls import path
from .views import ShowTable, CreateRodTemperatureTest, UpdateRodTemperatureTest, delete_rod

app_name = 'temperature_excursions'

urlpatterns = [
    path('<slug:rod_name>/', ShowTable.as_view(), name='table'),
    path('<slug:rod_name>/create_rod_temperature_test/', CreateRodTemperatureTest.as_view(), name='create'),
    path('update_rod_temperature_test/<slug:rod_name>/', UpdateRodTemperatureTest.as_view(), name='update'),
    path('delete_rod_temperature_test/<int:pk>/', delete_rod, name='delete'),
]