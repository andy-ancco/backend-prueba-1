from django.db import models
from datetime import date

# OPCIONES DE ÁREA (para que sea SELECT)
AREAS_CHOICES = [
    ('Urgencias', 'Urgencias'),
    ('Pediatría', 'Pediatría'),
    ('Cardiología', 'Cardiología'),
    ('Dermatología', 'Dermatología'),
    ('Radiología', 'Radiología'),
    ('Traumatología', 'Traumatología'),
]

# modelo que representara una visita en la base de datos 
class Visita(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)
    motivo_visita = models.TextField()
    hora_entrada = models.TimeField()
    hora_salida = models.TimeField()  # se puede ingresar la hora de forma manual
    fecha = models.DateField(default=date.today)  # se asigna el día automáticamente

    # NUEVOS CAMPOS:
    doctor = models.CharField(max_length=100, default="Sin asignar")
    area = models.CharField(max_length=50, choices=AREAS_CHOICES, default='Urgencias')

    def __str__(self):
        return f"{self.nombre} - {self.rut}"
