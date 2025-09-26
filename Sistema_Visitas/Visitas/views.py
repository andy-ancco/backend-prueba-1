from django.shortcuts import render, redirect, get_object_or_404
from .models import Visita
from .forms import VisitaForm

def lista_visitas(request):
    visitas = Visita.objects.all()
    return render(request, 'Visitas/lista_visitas.html', {'visitas': visitas})

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
    return render(request, 'Visitas/nueva_visita.html', {'form': form, 'mensaje_error': mensaje_error})

def eliminar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    visita.delete()
    return redirect('lista_visitas')
