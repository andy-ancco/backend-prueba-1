from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.db.models import Count
import os
from .models import Visita
from .forms import VisitaForm
from .serializers import VisitaSerializer

from groq import Groq

@login_required
def home(request):
    return render(request, "home.html")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_visitas(request):
    return Response({
        "total_visitas": Visita.objects.count(),
        "por_area": list(
            Visita.objects.values("area").annotate(total=Count("id"))
        ),
        "por_fecha": list(
            Visita.objects.values("fecha").annotate(total=Count("id"))
        ),
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recomendaciones_ia(request):
    client = Groq(api_key = os.getenv("GROQ_API_KEY"))

    total_visitas = Visita.objects.count()

    areas = (
        Visita.objects
        .values("area")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    resumen = "\n".join(
        [f"- {a['area']}: {a['total']} visitas" for a in areas]
    )

    prompt = f"""
    Eres un asistente que analiza datos de un sistema hospitalario.

    Total de visitas: {total_visitas}

    Visitas por área:
    {resumen}

    Genera recomendaciones breves y claras para mejorar la gestión del hospital.
    """

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    respuesta_ia = completion.choices[0].message.content

    return Response({
        "total_visitas": total_visitas,
        "analisis": areas,
        "recomendacion_ia": respuesta_ia
    })



class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer
    permission_classes = [IsAuthenticated]


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def eliminar_visita_api(request, id):
    try:
        visita = Visita.objects.get(id=id)
        visita.delete()
        return Response(
            {"mensaje": "Visita eliminada correctamente"},
            status=status.HTTP_200_OK
        )
    except Visita.DoesNotExist:
        return Response(
            {"error": "Visita no encontrada"},
            status=status.HTTP_404_NOT_FOUND
        )


@login_required
def lista_visitas(request):
    visitas = Visita.objects.all()
    return render(request, 'lista_visitas.html', {'visitas': visitas})


@login_required
def detalle_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    return render(request, 'detalle_visita.html', {'visita': visita})


@login_required
def nueva_visita(request):
    mensaje_error = ""
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_visitas')
        else:
            mensaje_error = "No se pudo guardar la visita. Revisa los datos."
    else:
        form = VisitaForm()

    return render(request, 'nueva_visita.html', {
        'form': form,
        'mensaje_error': mensaje_error
    })


@login_required
def editar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)

    if request.method == 'POST':
        form = VisitaForm(request.POST, instance=visita)
        if form.is_valid():
            form.save()
            return redirect('lista_visitas')
    else:
        form = VisitaForm(instance=visita)

    return render(request, 'editar_visita.html', {
        'form': form,
        'visita': visita
    })

@login_required
def eliminar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)

    if request.method == "POST":
        visita.delete()
        return redirect("lista_visitas")

    return render(request, "eliminar_visita.html", {
        "visita": visita
    })

@login_required
def panel_ia(request):
    visitas = (
        Visita.objects
        .values("area")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    total_visitas = Visita.objects.count()

    client = Groq(api_key=settings.GROQ_API_KEY)

    resumen = "\n".join(
        [f"- {v['area']}: {v['total']} visitas" for v in visitas]
    )

    prompt = f"""
    Analiza los siguientes datos hospitalarios:

    Total de visitas: {total_visitas}
    Visitas por área:
    {resumen}

    Genera recomendaciones breves para gestión hospitalaria.
    """

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    recomendacion = completion.choices[0].message.content

    return render(request, "panel_ia.html", {
        "total_visitas": total_visitas,
        "visitas": visitas,
        "recomendacion": recomendacion
    })