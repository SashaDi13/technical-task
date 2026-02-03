"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path

from realEstateAggregator.views import (
    AddPropertyView,
    DeletePropertyView,
    HomeView,
    RunScraperView,
    UpdatePropertyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('run_scrapper/', RunScraperView.as_view(), name='run_scrapper'),
    path('add_property/', AddPropertyView.as_view(), name='add_property'),
    path(
        'update_property/<str:id>', 
        UpdatePropertyView.as_view(), 
        name='update_property'
    ),
    path(
        'delete_property/<str:id>', 
        DeletePropertyView.as_view(), 
        name='delete_property'
    )
]
