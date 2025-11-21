from . import views
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register(r"Visita", views.VisitaViewSet)


# URLs principales del módulo de visitas
urlpatterns = [
    path("", views.lista_visitas, name="lista_visitas"),# Lista de visitas
    path("nueva/", views.nueva_visita, name="nueva_visita"),          # Crear nueva visita
    path("detalle/<int:id>/", views.detalle_visita, name="detalle_visita"),  # Ver detalle
    path("editar/<int:id>/", views.editar_visita, name="editar_visita"),     # Editar visita
    path("eliminar/<int:id>/", views.eliminar_visita, name="eliminar_visita"),  # Eliminar visita
    path("api/", include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]

