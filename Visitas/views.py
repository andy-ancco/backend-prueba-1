from django.shortcuts import render, redirect, get_object_or_404
from .models import Visita
from .forms import VisitaForm

#mostrar la listas de visitas
def lista_visitas(request):
    visitas = Visita.objects.all() #obtiene todas las visitas
    return render(request, 'lista_visitas.html', {'visitas': visitas})

#crear una nueva visita
def nueva_visita(request):
    mensaje_error = ""
    if request.method == 'POST':
        form = VisitaForm(request.POST) #crea el formulario con los datos enviados 
        if form.is_valid():
            form.save()
            return redirect('lista_visitas')
        else:
            mensaje_error = "No se pudo guardar la visita. Por favor revise los datos."
    else:
        form = VisitaForm()
    return render(request, 'nueva_visita.html', {'form': form, 'mensaje_error': mensaje_error})

#eliminar una visita existente
def eliminar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    visita.delete() #elimina la visita de la base de datos 
    return redirect('lista_visitas')
