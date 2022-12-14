"""Fuel_Rod_DB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fresh_inventory.urls')),
    path('temperature_excursions_exp/', include('temperature_excursions_exp.urls')),
    path('temperature_excursions/', include('temperature_excursions.urls')),
    path('dry_storage_exp/', include('dry_storage_exp.urls')),
    path('dry_storage/', include('dry_storage.urls')),
    path('rod_pieces/', include('rod_pieces.urls')),
]
