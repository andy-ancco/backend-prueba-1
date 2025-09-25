from django.shortcuts import render
from django.urls import path
from . import views

# Create your views here.
urlpatterns = [
    path("", views.lista_visitas, name="lista_visitas"),
    path("visitas/nuevo/", views.nueva_visita, name="nueva_visitas"),
]