from django.urls import path
from . import views

# URLs principales del módulo de visitas
urlpatterns = [
    path("", views.lista_visitas, name="lista_visitas"),              # Lista de visitas
    path("nueva/", views.nueva_visita, name="nueva_visita"),          # Crear nueva visita
    path("detalle/<int:id>/", views.detalle_visita, name="detalle_visita"),  # Ver detalle
    path("editar/<int:id>/", views.editar_visita, name="editar_visita"),     # Editar visita
    path("eliminar/<int:id>/", views.eliminar_visita, name="eliminar_visita"),  # Eliminar visita
]

