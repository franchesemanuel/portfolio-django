from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import bleach

MAX_IMAGE_SIZE_BYTES = 2 * 1024 * 1024
ALLOWED_IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}


def sanitize_text(value):
    """Sanitiza texto removiendo HTML para prevenir XSS almacenado."""
    if value is None:
        return value
    return bleach.clean(value, tags=[], attributes={}, strip=True).strip()


def validate_image_size(file):
    """Valida el tamaño máximo de imagen."""
    if file.size > MAX_IMAGE_SIZE_BYTES:
        raise ValidationError("La imagen supera el tamaño máximo permitido (2MB).")


def validate_image_mime_type(file):
    """Valida el tipo MIME de la imagen subida."""
    content_type = getattr(file, "content_type", None)
    if content_type and content_type.lower() not in ALLOWED_IMAGE_MIME_TYPES:
        raise ValidationError("Tipo de imagen no permitido. Usa JPG, PNG o WEBP.")


class Profile(models.Model):
    """
    Modelo Singleton para datos del perfil del desarrollador.
    Solo debe haber una instancia activa en la BD.
    """
    # Información personal
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre Completo",
        default="Franco Emanuel Salcedo"
    )
    titulo_profesional = models.CharField(
        max_length=200,
        verbose_name="Título Profesional",
        default="Desarrollador Django + Especialista en Ciberseguridad",
        help_text="Ej: 'Desarrollador Senior' o 'Full Stack Developer'"
    )
    subtitulo_header = models.CharField(
        max_length=300,
        verbose_name="Subtítulo del Header",
        default="Creo aplicaciones web seguras, escalables y profesionales",
        help_text="Texto que aparece debajo del nombre en el hero"
    )
    
    # Imagen de perfil
    foto_perfil = models.ImageField(
        upload_to='profile/',
        verbose_name="Foto de Perfil",
        null=True,
        blank=True,
        help_text="Imagen principal del perfil (JPG o PNG, min 400x400px)",
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
            validate_image_mime_type,
        ]
    )
    
    # Biografía y descripción
    descripcion_corta = models.CharField(
        max_length=200,
        verbose_name="Descripción Corta",
        default="Desarrollo web con seguridad integrada desde el primer día",
        help_text="Texto para cards y meta descripciones"
    )
    
    bio = models.TextField(
        verbose_name="Biografía Completa",
        default="Soy un desarrollador apasionado por crear soluciones web seguras y escalables.",
        help_text="Texto que aparece en la sección 'Sobre mí'"
    )
    
    filosofia = models.TextField(
        verbose_name="Filosofía de Desarrollo",
        default="Creo que la seguridad no es un add-on, es un principio fundamental.",
        help_text="Blockquote en la sección 'Sobre mí'"
    )
    
    # Tecnologías
    tecnologias = models.TextField(
        verbose_name="Tecnologías Principales",
        default="Django, Python, PostgreSQL, REST APIs, Docker, Linux",
        help_text="Separadas por coma o salto de línea"
    )
    
    # Contacto
    email = models.EmailField(
        verbose_name="Email",
        default="franco@example.com",
        help_text="Email de contacto principal"
    )
    telefono = models.CharField(
        max_length=20,
        verbose_name="Teléfono",
        blank=True,
        default="+34 600 000 000",
        help_text="Formato: +34 600 000 000"
    )
    ciudad = models.CharField(
        max_length=100,
        verbose_name="Ciudad/País",
        blank=True,
        default="España",
        help_text="Ubicación geográfica"
    )
    
    # Redes sociales
    github_url = models.URLField(
        verbose_name="GitHub",
        blank=True,
        default="https://github.com/franchesemanuel",
        help_text="URL completa a tu perfil de GitHub"
    )
    linkedin_url = models.URLField(
        verbose_name="LinkedIn",
        blank=True,
        default="https://linkedin.com/in/franco",
        help_text="URL completa a tu perfil de LinkedIn"
    )
    twitter_url = models.URLField(
        verbose_name="Twitter/X",
        blank=True,
        default="",
        help_text="URL completa a tu perfil de Twitter"
    )
    
    # Información adicional
    cv_url = models.URLField(
        verbose_name="CV/Currículum",
        blank=True,
        default="",
        help_text="URL a tu CV descargable"
    )
    
    # Secciones activas
    mostrar_blog = models.BooleanField(
        default=False,
        verbose_name="¿Mostrar sección Blog?"
    )
    mostrar_testimonios = models.BooleanField(
        default=False,
        verbose_name="¿Mostrar sección Testimonios?"
    )
    
    # Metadata
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="¿Perfil Activo?"
    )
    
    class Meta:
        verbose_name = "Perfil del Desarrollador"
        verbose_name_plural = "Perfil del Desarrollador"
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        """
        Asegurar que solo haya un Profile activo.
        Si se intenta guardar otro con activo=True, desactivar los demás.
        """
        self.nombre = sanitize_text(self.nombre)
        self.titulo_profesional = sanitize_text(self.titulo_profesional)
        self.subtitulo_header = sanitize_text(self.subtitulo_header)
        self.descripcion_corta = sanitize_text(self.descripcion_corta)
        self.bio = sanitize_text(self.bio)
        self.filosofia = sanitize_text(self.filosofia)
        self.tecnologias = sanitize_text(self.tecnologias)
        self.email = sanitize_text(self.email)
        self.telefono = sanitize_text(self.telefono)
        self.ciudad = sanitize_text(self.ciudad)
        self.github_url = sanitize_text(self.github_url)
        self.linkedin_url = sanitize_text(self.linkedin_url)
        self.twitter_url = sanitize_text(self.twitter_url)
        self.cv_url = sanitize_text(self.cv_url)
        if self.activo:
            # Desactivar todos los demás perfiles activos
            Profile.objects.filter(activo=True).exclude(pk=self.pk).update(activo=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active(cls):
        """Obtener el perfil activo (singleton pattern)"""
        profile, created = cls.objects.get_or_create(
            activo=True,
            defaults={
                'nombre': 'Franco Emanuel Salcedo',
                'titulo_profesional': 'Desarrollador Django + Especialista en Ciberseguridad',
            }
        )
        return profile


class Project(models.Model):
    """
    Modelo para proyectos del portafolio.
    Permite agregar, editar y eliminar proyectos desde admin.
    """
    # Información básica
    titulo = models.CharField(
        max_length=200,
        verbose_name="Título del Proyecto"
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="Slug",
        help_text="URL amigable (ej: mi-proyecto-web)"
    )
    descripcion_corta = models.CharField(
        max_length=300,
        verbose_name="Descripción Corta",
        help_text="Se muestra en la tarjeta del proyecto"
    )
    descripcion_completa = models.TextField(
        verbose_name="Descripción Completa",
        blank=True,
        help_text="Descripción detallada del proyecto (opcional)"
    )
    
    # Imagen
    imagen = models.ImageField(
        upload_to='projects/',
        verbose_name="Imagen del Proyecto",
        help_text="Dimensiones recomendadas: 800x600px",
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
            validate_image_mime_type,
        ]
    )
    
    # Tecnologías/Tags
    tecnologias = models.CharField(
        max_length=300,
        verbose_name="Tecnologías Utilizadas",
        help_text="Separadas por coma. Ej: Django, PostgreSQL, Docker"
    )
    
    # Enlaces
    demo_url = models.URLField(
        verbose_name="Link Demo/Live",
        blank=True,
        help_text="URL donde se puede ver el proyecto en vivo"
    )
    github_url = models.URLField(
        verbose_name="Link GitHub",
        blank=True,
        help_text="URL del repositorio en GitHub"
    )
    
    # Ordenamiento y visibilidad
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden de aparición",
        help_text="Proyectos con número menor aparecen primero"
    )
    visible = models.BooleanField(
        default=True,
        verbose_name="¿Visible en portafolio?"
    )
    
    # Metadata
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    
    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['orden', '-fecha_creacion']
    
    def __str__(self):
        return self.titulo
    
    def get_tecnologias_list(self):
        """Retorna lista de tecnologías"""
        return [t.strip() for t in self.tecnologias.split(',')]

    def save(self, *args, **kwargs):
        self.titulo = sanitize_text(self.titulo)
        self.descripcion_corta = sanitize_text(self.descripcion_corta)
        self.descripcion_completa = sanitize_text(self.descripcion_completa)
        self.tecnologias = sanitize_text(self.tecnologias)
        self.demo_url = sanitize_text(self.demo_url)
        self.github_url = sanitize_text(self.github_url)
        super().save(*args, **kwargs)


class Service(models.Model):
    """
    Modelo para servicios ofrecidos.
    Muestra qué tipos de servicios puedes ofrecer.
    """
    icono = models.CharField(
        max_length=100,
        verbose_name="Icono FontAwesome",
        help_text="Ej: fas fa-code, fas fa-shield-alt"
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del Servicio",
        help_text="Ej: Desarrollo Web"
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción del servicio"
    )
    orden = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden de aparición"
    )
    visible = models.BooleanField(
        default=True,
        verbose_name="¿Visible?"
    )
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.icono = sanitize_text(self.icono)
        self.nombre = sanitize_text(self.nombre)
        self.descripcion = sanitize_text(self.descripcion)
        super().save(*args, **kwargs)


class SiteSettings(models.Model):
    """
    Configuración general del sitio.
    Singleton: solo una instancia debe existir.
    """
    # SEO y Metadata
    titulo_sitio = models.CharField(
        max_length=100,
        verbose_name="Título del Sitio",
        default="Franco Emanuel - Desarrollador Django + Ciberseguridad"
    )
    descripcion_sitio = models.CharField(
        max_length=160,
        verbose_name="Descripción (Meta)",
        default="Portfolio profesional de desarrollador Django especializado en ciberseguridad"
    )
    
    # Textos secciones
    titulo_seccion_proyectos = models.CharField(
        max_length=200,
        verbose_name="Título Sección Proyectos",
        default="Mis Proyectos"
    )
    descripcion_seccion_proyectos = models.TextField(
        verbose_name="Descripción Sección Proyectos",
        blank=True,
        default="Proyectos que muestran mi expertise en desarrollo seguro y escalable"
    )
    
    titulo_seccion_servicios = models.CharField(
        max_length=200,
        verbose_name="Título Sección Servicios",
        default="¿Qué Ofrezco?"
    )
    descripcion_seccion_servicios = models.TextField(
        verbose_name="Descripción Sección Servicios",
        blank=True,
        default="Servicios profesionales para tu proyecto"
    )
    
    # Footer
    texto_footer = models.TextField(
        verbose_name="Texto Footer",
        default="© 2026 Franco Emanuel Salcedo. Todos los derechos reservados.",
        help_text="Texto que aparece al pie de página"
    )
    
    # Secciones activas globales
    mostrar_projects = models.BooleanField(
        default=True,
        verbose_name="¿Mostrar sección Proyectos?"
    )
    mostrar_services = models.BooleanField(
        default=True,
        verbose_name="¿Mostrar sección Servicios?"
    )
    mostrar_contact = models.BooleanField(
        default=True,
        verbose_name="¿Mostrar formulario de contacto?"
    )
    
    # Analytics (opcionales)
    google_analytics_id = models.CharField(
        max_length=50,
        verbose_name="Google Analytics ID",
        blank=True,
        default=""
    )
    
    actualizado = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    
    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuración del Sitio"
    
    def __str__(self):
        return "Configuración General"
    
    @classmethod
    def get_settings(cls):
        """Obtener configuración activa (singleton pattern)"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

    def save(self, *args, **kwargs):
        self.titulo_sitio = sanitize_text(self.titulo_sitio)
        self.descripcion_sitio = sanitize_text(self.descripcion_sitio)
        self.titulo_seccion_proyectos = sanitize_text(self.titulo_seccion_proyectos)
        self.descripcion_seccion_proyectos = sanitize_text(self.descripcion_seccion_proyectos)
        self.titulo_seccion_servicios = sanitize_text(self.titulo_seccion_servicios)
        self.descripcion_seccion_servicios = sanitize_text(self.descripcion_seccion_servicios)
        self.texto_footer = sanitize_text(self.texto_footer)
        self.google_analytics_id = sanitize_text(self.google_analytics_id)
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    """Modelo original mantenido para compatibilidad"""
    name = models.CharField(max_length=100, verbose_name="Nombre")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Asunto", blank=True, null=True)
    message = models.TextField(verbose_name="Mensaje")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    leido = models.BooleanField(default=False, verbose_name="¿Leído?")

    def __str__(self):
        return f"Mensaje de {self.name} - {self.email}"

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.name = sanitize_text(self.name)
        self.email = sanitize_text(self.email)
        self.subject = sanitize_text(self.subject)
        self.message = sanitize_text(self.message)
        super().save(*args, **kwargs)
