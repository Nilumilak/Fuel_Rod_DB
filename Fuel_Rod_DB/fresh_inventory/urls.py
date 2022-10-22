from django.urls import path
from .views import ShowTable

app_name = 'fresh_inventory'

urlpatterns = [
    path('', ShowTable.as_view()),
    path('fresh_inventory/', ShowTable.as_view(), name='table'),
]