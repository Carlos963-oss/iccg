from collections import defaultdict
from django.shortcuts import render
from .models import EventoDestacado, EventoLateral,Ministerio,FotoMinisterio,Horario,Aviso,Hero


# 🎨 Colores por categoría
CAT_COLORES = {
    "Servicio":       {"bg": "#eef2ff", "color": "#3730a3", "dot": "#6366f1"},
    "Retiro":         {"bg": "#f0fdf4", "color": "#166534", "dot": "#22c55e"},
    "Conferencia":    {"bg": "#fff7ed", "color": "#9a3412", "dot": "#f97316"},
    "Taller bíblico": {"bg": "#fef9c3", "color": "#854d0e", "dot": "#eab308"},
    "Congreso":       {"bg": "#fdf4ff", "color": "#7e22ce", "dot": "#a855f7"},
    "Campamento":     {"bg": "#ecfdf5", "color": "#065f46", "dot": "#10b981"},
    "Otro":           {"bg": "#f5f5f5", "color": "#555555", "dot": "#999999"},
}

def inicio(request):

    # 🔥 EVENTO PRINCIPAL
    evento = EventoDestacado.objects.filter(
        activo=True
    ).order_by('-creado').first()

    # 🔥 EVENTOS LATERALES
    eventos_laterales = EventoLateral.objects.filter(
        activo=True
    ).order_by('orden')[:2]

    # 👉 AQUÍ INTEGRAMOS LOS COLORES
    for ev in eventos_laterales:
        c = CAT_COLORES.get(ev.categoria, CAT_COLORES["Otro"])
        ev.cat_bg = c["bg"]
        ev.cat_color = c["color"]
        ev.cat_dot = c["dot"]

    # 🔥 HORARIOS
    horarios = Horario.objects.select_related('tipo')
    agrupados = defaultdict(list)

    for h in horarios:
        agrupados[h.tipo.nombre].append(h)

    # 🔥 AVISO
    aviso = Aviso.objects.filter(activo=True).first()

    # 🔥 HERO
    hero = Hero.objects.filter(activo=True).first()

    # 🔥 CONTEXTO FINAL
    return render(request, "core/inicio.html", {
        'evento': evento,
        'eventos_laterales': eventos_laterales,
        'horarios_agrupados': dict(agrupados),
        'aviso': aviso,
        'hero': hero 
    })
def color_azul(request):
    return render(request, 'core/color_azul.html')

def color_rojo(request):
    return render(request, 'core/color_rojo.html')

def color_amarillo(request):
    return render(request, 'core/color_amarillo.html')

def color_morado(request):
    return render(request, 'core/color_morado.html')

def ministerio_detalle(request, id):
    ministerio = Ministerio.objects.get(id=id)
    fotos = FotoMinisterio.objects.filter(ministerio=ministerio)

    return render(request, 'core/ministerio.html', {
        'ministerio': ministerio,
        'fotos': fotos
    })
    
def Nuestro_origen(request):
    return render(request, 'core/Nuestro_origen.html')

def Nuestra_casa(request):
    return render(request, 'core/Nuestra_casa.html')