from django.urls import path
from .views import ShowTable, CreateRodDryStorageTest, UpdateRodDryStorageTest

app_name = 'dry_storage'

urlpatterns = [
    path('<slug:rod_name>/', ShowTable.as_view(), name='table'),
    path('<slug:rod_name>/create_rod_dry_storage_test/', CreateRodDryStorageTest.as_view(), name='create'),
    path('update_rod_dry_storage_test/<slug:rod_name>/', UpdateRodDryStorageTest.as_view(), name='update'),
]