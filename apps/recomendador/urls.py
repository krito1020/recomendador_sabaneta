# URLs de app
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='recomendador_home'),
    path('registro/', views.registrar_comercio, name='registro'),
]
