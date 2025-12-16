from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from . import views

router = routers.DefaultRouter()
router.register(r"visitas", views.VisitaViewSet, basename="visita")


urlpatterns = [
    path("", views.home, name="home"),
    path("visitas/", views.lista_visitas, name="lista_visitas"),
    path("visitas/nueva/", views.nueva_visita, name="nueva_visita"),
    path("visitas/detalle/<int:id>/", views.detalle_visita, name="detalle_visita"),
    path("visitas/editar/<int:id>/", views.editar_visita, name="editar_visita"),
    path("visitas/eliminar/<int:id>/", views.eliminar_visita, name="eliminar_visita"),
    path("panel-ia/", views.panel_ia, name="ia_recomendaciones"),
    path("dashboard/", views.dashboard_visitas, name="dashboard"),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("accounts/", include("django.contrib.auth.urls")),

]
