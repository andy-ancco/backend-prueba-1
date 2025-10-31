from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from .models import Visita
import csv


@admin.action(description="Exportar visitas seleccionadas a CSV (compatible con Excel)")
def exportar_visitas_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="visitas.csv"'
    response.write('\ufeff')  # para que se abra bien en Excel
    writer = csv.writer(response, delimiter=';')
    writer.writerow(["ID", "Nombre", "RUT", "Motivo", "Fecha", "Hora Entrada", "Hora Salida"])
    for v in queryset:
        writer.writerow([
            v.id,
            v.nombre,
            v.rut,
            v.motivo_visita,
            v.fecha.strftime('%Y-%m-%d'),
            v.hora_entrada.strftime('%H:%M') if v.hora_entrada else '',
            v.hora_salida.strftime('%H:%M') if v.hora_salida else '',
        ])
    return response


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'fecha', 'motivo_visita', 'motivo_corto', 'hora_entrada', 'hora_salida')
    list_editable = ('motivo_visita',)
    search_fields = ('nombre', 'rut', 'motivo_visita')
    list_filter = ('fecha',)
    ordering = ('-fecha', 'hora_entrada')
    list_per_page = 25
    actions = [exportar_visitas_csv]

    fieldsets = (
        ('Datos personales', {'fields': ('nombre', 'rut')}),
        ('Detalles de la visita', {
            'fields': ('motivo_visita', 'fecha', 'hora_entrada', 'hora_salida'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Motivo (Resumen)')
    def motivo_corto(self, obj):
        return (obj.motivo_visita[:40] + '...') if len(obj.motivo_visita) > 40 else obj.motivo_visita

    # ✅ Validación tipo inline (sin romper la página ni redirigir)
    def save_model(self, request, obj, form, change):
        errores = []

        # Validar que la hora de salida sea posterior a la hora de entrada
        if obj.hora_entrada and obj.hora_salida:
            if obj.hora_salida <= obj.hora_entrada:
                errores.append("⚠️ La hora de salida debe ser posterior a la hora de entrada.")

        # Validar duplicado de RUT + fecha
        if not change:
            if Visita.objects.filter(rut=obj.rut, fecha=obj.fecha).exists():
                errores.append(f"ℹ️ Ya existe una visita registrada para el RUT {obj.rut} en la fecha {obj.fecha}.")

        # Si hay errores, mostrar y no guardar
        if errores:
            for e in errores:
                self.message_user(request, e, level=messages.ERROR)
            return  # ❌ evita guardar el registro

        # ✅ Si todo está bien, guarda normalmente
        super().save_model(request, obj, form, change)