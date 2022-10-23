from django.urls import path
from .views import ShowTable

app_name = 'dry_storage'

urlpatterns = [
    path('', ShowTable.as_view(), name='table'),
]