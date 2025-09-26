from django import forms
from .models import Visita
import re

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['nombre', 'rut', 'motivo_visita', 'hora_entrada', 'hora_salida']
        widgets = {
            'motivo_visita': forms.Textarea(
                attrs={'rows': 4, 'placeholder': 'Ingrese el motivo de la visita...'}
            ),
        }
        
        error_messages = {
            'hora_entrada': {
                'required': 'Por favor, ingresa la hora de entrada.',
            },
            'hora_salida': {
                'required': 'Por favor, ingresa la hora de salida.',
            },
            'nombre': {
                'required': 'El nombre es obligatorio.',
            },
            'rut': {
                'required': 'El RUT es obligatorio.',
            },
        }

    # --- Validación personalizada para el RUT ---
    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        # 1. Validar formato básico con puntos y guion
        patron = r'^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$'
        if not re.match(patron, rut):
            raise forms.ValidationError("Formato incorrecto. Ejemplo: 12.345.678-9")

        # 2. Eliminar puntos y guion para validar el dígito verificador
        rut = rut.replace(".", "").replace("-", "").upper()

        if len(rut) < 2:
            raise forms.ValidationError("RUT demasiado corto.")

        num, dv = rut[:-1], rut[-1]

        try:
            num = int(num)
        except ValueError:
            raise forms.ValidationError("RUT inválido.")

        # 3. Calcular el dígito verificador
        suma = 0
        multiplicador = 2
        for digit in reversed(str(num)):
            suma += int(digit) * multiplicador
            multiplicador += 1
            if multiplicador > 7:
                multiplicador = 2

        dv_calculado = 11 - (suma % 11)
        if dv_calculado == 11:
            dv_calculado = "0"
        elif dv_calculado == 10:
            dv_calculado = "K"
        else:
            dv_calculado = str(dv_calculado)

        if dv != dv_calculado:
            raise forms.ValidationError("RUT inválido, el dígito verificador no coincide.")

        return f"{str(num)}-{dv}"
