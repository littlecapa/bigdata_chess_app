"""chess URL Configuration

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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.main_page, name="main_page"),
    path('twic/', views.display_twic_status, name='display_twic_status'),
    path('download/', views.download_twic, name='download_twic'),
    path('lisplit/', views.lisplit, name='lisplit'),
    path('liprocess/', views.liprocess, name='liprocess'),
    path('liconcat/', views.liconcat, name='liconcat'),
    path('execute_split/', views.execute_split, name='execute_split'),
]

