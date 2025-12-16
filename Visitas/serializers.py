from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Visita

class VisitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visita
        fields = "__all__"



class GroupSerializer:
    class Meta:
        model = Group
        fields = ["url", "name"]