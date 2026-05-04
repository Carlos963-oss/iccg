from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from cloudinary.models import CloudinaryField


class EventoDestacado(models.Model):
    titulo_superior = models.CharField(max_length=100, blank=True)
    titulo_principal = models.CharField(max_length=200)

    imagen = CloudinaryField(verbose_name="Imagen PC")
    imagen_movil = CloudinaryField(blank=True, null=True, verbose_name="Imagen celular")

    posicion_imagen = models.CharField(
        max_length=20,
        choices=[
            ("center", "Centro"),
            ("top", "Arriba"),
            ("bottom", "Abajo"),
        ],
        default="center"
    )

    color_titulo = models.CharField(max_length=7, default="#f6ff00")
    color_subtitulo = models.CharField(max_length=7, default="#cbf5e4")
    color_contador = models.CharField(max_length=7, default="#ffffff")

    fecha_evento = models.DateTimeField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.activo and not self.fecha_evento:
            raise ValidationError("Si el evento está activo, debes asignar una fecha.")

        if self.fecha_evento and self.fecha_evento < timezone.now():
            raise ValidationError("La fecha del evento no puede ser en el pasado.")

    def save(self, *args, **kwargs):
        if not self.activo:
            self.fecha_evento = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo_principal


class EventoLateral(models.Model):
    CATEGORIA_CHOICES = [
        ("Servicio", "Servicio"),
        ("Retiro", "Retiro"),
        ("Conferencia", "Conferencia"),
        ("Taller bíblico", "Taller bíblico"),
        ("Congreso", "Congreso"),
        ("Campamento", "Campamento"),
        ("Otro", "Otro"),
    ]

    titulo = models.CharField(max_length=200)
    imagen = CloudinaryField('image')  # 🔥 cambiado
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES, default="Servicio")
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["orden", "fecha"]

    def __str__(self):
        return self.titulo

    def clean(self):
        if self.fecha:
            hoy = timezone.localdate()
            if self.fecha < hoy:
                raise ValidationError("No puedes seleccionar una fecha pasada.")


class Ministerio(models.Model):
    nombre = models.CharField(max_length=100)
    lider = models.CharField(max_length=100)
    descripcion = models.TextField()

    imagen = CloudinaryField( verbose_name="Imagen perfil")  
    portada = CloudinaryField( verbose_name="Imagen portada")  

    def __str__(self):
        return self.nombre


class FotoMinisterio(models.Model):
    ministerio = models.ForeignKey(Ministerio, on_delete=models.CASCADE)
    imagen = CloudinaryField('image')

    def __str__(self):
        return f"Foto de {self.ministerio.nombre}"


class TipoServicio(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Horario(models.Model):
    DIAS = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miercoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sabado'),
        ('domingo', 'Domingo'),
    ]

    ORDEN_DIAS = {
        'lunes': 1,
        'martes': 2,
        'miercoles': 3,
        'jueves': 4,
        'viernes': 5,
        'sabado': 6,
        'domingo': 7,
    }

    dia = models.CharField(max_length=10, choices=DIAS)
    hora = models.CharField(max_length=50)

    tipo = models.ForeignKey(
        TipoServicio,
        on_delete=models.CASCADE,
        related_name='horarios'
    )

    def orden(self):
        return self.ORDEN_DIAS[self.dia]

    def __str__(self):
        return f"{self.tipo.nombre} - {self.get_dia_display()} {self.hora}"


class Aviso(models.Model):
    TIPOS = [
        ('urgente', 'Urgente'),
        ('importante', 'Importante'),
        ('informativo', 'Informativo'),
    ]

    titulo = models.CharField(max_length=100)
    mensaje = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    texto_boton = models.CharField(max_length=50, default="Entendido")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class Hero(models.Model):

    TIPO_FONDO = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
    ]

    tipo_fondo = models.CharField(max_length=10, choices=TIPO_FONDO, default='imagen')
    imagen = CloudinaryField(verbose_name="para moviles")
    video = CloudinaryField(
        resource_type='video',
        blank=True,
        null=True,
        verbose_name="Video PC"
    )

    activo = models.BooleanField(default=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.activo:
            Hero.objects.update(activo=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Hero {self.id} - {self.tipo_fondo}"

    class Meta:
        ordering = ['-fecha']