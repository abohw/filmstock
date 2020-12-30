"""vch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import re_path, path, include
from web import views
from django.views.generic.base import TemplateView
from django_filters.views import FilterView
from web.models import Camera

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    re_path(r'^save$', views.saveSearch, name='save-search'),
    re_path(r'^cameras$', views.cameras, name='cameras'),
    path('film/', views.film, name='film'),
    path('users/', include('hunters.urls')),
    path('users/', include('django.contrib.auth.urls')),
]
