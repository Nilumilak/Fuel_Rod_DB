from django.urls import path
from .views import ShowTable, CreateDryStorageExp, UpdateDryStorageExp

app_name = 'dry_storage_exp'

urlpatterns = [
    path('', ShowTable.as_view(), name='table'),
    path('create_dry_storage_exp/', CreateDryStorageExp.as_view(), name='create'),
    path('update_dry_storage_exp/<slug:rod_name>/', UpdateDryStorageExp.as_view(), name='update'),
]