"""vv_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.main_page, name='Main Page'),
    path('anacapa/', views.anacapa, name='Anacapa'),
    path('mrdna/', views.mrdna, name='MrDNA'),
    path('qiime2/', views.qiime2, name='QIIME2'),
    path('piphillin/<int:num>/', views.piphillin, name='Piphillin'),
    path('output/', views.output_view, name='Output'),
    path('output_download/<slug:directory>/', views.get_output, name='Output Download'),
    path('display_log/<slug:directory>/', views.display_log, name='Display Log'),
]