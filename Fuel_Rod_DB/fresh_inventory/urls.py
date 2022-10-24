from django.urls import path
from .views import ShowTable, CreateRawRod, LoginUser, logout_user, RegistrationUser

app_name = 'fresh_inventory'

urlpatterns = [
    path('', ShowTable.as_view()),
    path('fresh_inventory/', ShowTable.as_view(), name='table'),
    path('fresh_inventory/create_raw_rod/', CreateRawRod.as_view(), name='create'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegistrationUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
]