from django.urls import path
from .views import ShowTable

app_name = 'rod_pieces'

urlpatterns = [
    path('<slug:rod_name>/', ShowTable.as_view(), name='table'),
]