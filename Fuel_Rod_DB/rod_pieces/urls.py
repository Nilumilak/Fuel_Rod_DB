from django.urls import path
from .views import ShowTable, CreateRodPiece

app_name = 'rod_pieces'

urlpatterns = [
    path('<slug:rod_name>/', ShowTable.as_view(), name='table'),
    path('<slug:rod_name>/create_rod_piece/', CreateRodPiece.as_view(), name='create'),
]