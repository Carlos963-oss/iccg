from django.contrib import admin
from django import forms
from .models import (
    EventoDestacado, EventoLateral,
    Ministerio, FotoMinisterio,
    Horario, TipoServicio,
    Aviso, Hero
)

class EventoDestacadoForm(forms.ModelForm):

    fecha_evento = forms.DateTimeField(
        required=False, 
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local'
            }
        )
    )

    class Meta:
        model = EventoDestacado
        fields = "__all__"
        widgets = {
            'color_titulo': forms.TextInput(attrs={'type': 'color'}),
            'color_subtitulo': forms.TextInput(attrs={'type': 'color'}),
            'color_contador': forms.TextInput(attrs={'type': 'color'}),
        }

class EventoLateralForm(forms.ModelForm):

    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'}
        )
    )

    hora = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'type': 'time'}
        )
    )

    class Meta:
        model = EventoLateral
        fields = "__all__"
        
        
@admin.register(EventoLateral)
class EventoLateralAdmin(admin.ModelAdmin):

    form = EventoLateralForm  

    list_display       = ("titulo", "categoria", "fecha", "hora", "orden", "activo")
    list_editable      = ("orden", "activo")
    list_display_links = ("titulo",)
    list_filter        = ("activo", "categoria", "fecha")
    search_fields      = ("titulo",)
    ordering           = ("orden", "fecha")
    
    
    

@admin.register(EventoDestacado)
class EventoDestacadoAdmin(admin.ModelAdmin):
    form = EventoDestacadoForm

    list_display = ("titulo_principal", "fecha_evento", "activo")

    fieldsets = (
        ("Contenido", {
            "fields": ("titulo_superior", "titulo_principal")
        }),
        ("Diseño", {
            "fields": (
                "imagen",
                "imagen_movil",
                "posicion_imagen",
                "color_titulo",
                "color_subtitulo",
                "color_contador"
            )
        }),
        ("Configuración", {
            "fields": ("fecha_evento", "activo")
        }),
    )

# ================= MINISTERIOS =================
class FotoInline(admin.TabularInline):
    model = FotoMinisterio
    extra = 1


@admin.register(Ministerio)
class MinisterioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "lider")
    search_fields = ("nombre", "lider")
    inlines = [FotoInline]


admin.site.register(FotoMinisterio)


# ================= TIPOS DE SERVICIO =================
@admin.register(TipoServicio)
class TipoServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


# ================= HORARIOS =================
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("tipo", "dia", "hora")
    list_filter = ("tipo", "dia")
    ordering = ("tipo", "dia")
    search_fields = ("tipo__nombre",)


# ================= AVISOS =================
@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "tipo", "activo")
    list_filter = ("tipo", "activo")
    search_fields = ("titulo", "mensaje")


# ================= HERO =================
@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ("id", "tipo_fondo", "activo", "fecha")
    list_editable = ("activo",)
    ordering = ("-fecha",)

    fieldsets = (
        ("Tipo de fondo", {
            "fields": ("tipo_fondo",)
        }),
        ("Contenido", {
            "fields": ("imagen", "video"),
            "description": "Sube imagen siempre. El video es opcional."
        }),
        ("Estado", {
            "fields": ("activo",)
        }),
    )