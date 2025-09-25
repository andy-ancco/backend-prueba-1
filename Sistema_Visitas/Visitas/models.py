from django.db import models

# Create your models here.
class Visita(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=False)
    fecha = models.DateField(auto_now_add=True)
    motivo = models.TextField()
    hora_entrada = models.TimeField(auto_now_add=True)
    hora_salida = models.TimeField()
    
