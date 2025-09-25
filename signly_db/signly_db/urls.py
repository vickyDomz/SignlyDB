"""
URL configuration for signly_db project.

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
from django.contrib.auth import views as auth_views
from signs import views
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign_list/', views.sign_list, name='sign_list'),
    path('sign_detail/<int:pk>/', views.sign_detail, name="sign_detail"),
    path('sign_edit/<int:pk>/', views.sign_edit, name='sign_edit'),
    path('sign_new/', views.sign_new, name='sign_new'),
    path('signVideo_list/', views.signVideo_list, name='signVideo_list'),
    path('signVideo_detail/<int:pk>/', views.signVideo_detail, name='signVideo_detail'),
    path('signVideo_edit/<int:pk>/', views.signVideo_edit, name='signVideo_edit'),
    path('signVideo_new/', views.signVideo_new, name='signVideo_new'),
    path('signVideo_estadoF/<int:pk>/', views.signVideo_estadoF, name='signVideo_estadoF'),
    path('signVideo_estadoT/<int:pk>/', views.signVideo_estadoT, name='signVideo_estadoT'),
    path('signVideo_ap_reF/<int:pk>/', views.signVideo_ap_reF, name='signVideo_ap_reF'),
    path('signVideo_ap_reT/<int:pk>/', views.signVideo_ap_reT, name='signVideo_ap_reT'),
    path('trainingMod_list/', views.trainingMod_list, name='trainingMod_list'),
    path('trainingMod_detail/<int:pk>/', views.trainingMod_detail, name="trainingMod_detail"),
    path('trainingMod_edit/<int:pk>/', views.trainingMod_edit, name='trainingMod_edit'),
    path('trainingMod_new/', views.trainingMod_new, name='trainingMod_new'),
    path('etiqueta_list/', views.etiqueta_list, name='etiqueta_list'),
    path('etiqueta_detail/<int:pk>/', views.etiqueta_detail, name="etiqueta_detail"),
    path('etiqueta_edit/<int:pk>/', views.etiqueta_edit, name='etiqueta_edit'),
    path('etiqueta_new/', views.etiqueta_new, name='etiqueta_new'),
    path('procesar_videos/', views.procesar_videos, name='procesar_videos'),
]
