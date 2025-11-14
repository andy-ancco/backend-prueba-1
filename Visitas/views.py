from django.shortcuts import render, redirect, get_object_or_404
from .models import Visita
from .forms import VisitaForm

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from .serializers import GroupSerializer, VisitaSerializer


class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all().order_by("nombre")
    serializers_class = VisitaSerializer
    permission_classes = [permissions.IsAuthenticated]

# Mostrar la lista de visitas
def lista_visitas(request):
    visitas = Visita.objects.all()
    return render(request, 'lista_visitas.html', {'visitas': visitas})

# Ver el detalle de una visita específica
def detalle_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    return render(request, 'detalle_visita.html', {'visita': visita})

# Crear una nueva visita
def nueva_visita(request):
    mensaje_error = ""
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_visitas')
        else:
            mensaje_error = "No se pudo guardar la visita. Por favor revise los datos."
    else:
        form = VisitaForm()
    return render(request, 'nueva_visita.html', {'form': form, 'mensaje_error': mensaje_error})

# Editar una visita existente
def editar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    if request.method == 'POST':
        form = VisitaForm(request.POST, instance=visita)
        if form.is_valid():
            form.save()
            return redirect('lista_visitas')
    else:
        form = VisitaForm(instance=visita)
    return render(request, 'editar_visita.html', {'form': form, 'visita': visita})

# Eliminar una visita (con confirmación)
def eliminar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    if request.method == 'POST':
        visita.delete()
        return redirect('lista_visitas')
    return render(request, 'eliminar_visita.html', {'visita': visita})
