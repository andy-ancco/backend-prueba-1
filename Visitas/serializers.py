from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Visita

class VisitaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Visita
        fields = ["url","nombre", "rut", "motivo_visita", "hora_entrada", "hora_salida", "fecha"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]