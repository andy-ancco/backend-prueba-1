from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Visita

#admin.site.register(Visita)

@admin.register(Visita)
class VisitasAdmin(admin.ModelAdmin):
    list_display = ('nombre','rut','fecha','motivo_visita')
    list_filter = ('fecha',)
    search_fields = ('nombre','rut')
    list_editable = ('motivo_visita',)
    ordering = ('fecha',)
    readonly_fields = ('hora_entrada','hora_salida')

    fieldsets = (
        ('Persona', {'fields': ('nombre', 'rut')})
                ,)