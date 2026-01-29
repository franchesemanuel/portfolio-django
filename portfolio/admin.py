from django.contrib import admin
from django.utils.html import format_html
from .admin_site import admin_site
from .models import Profile, Project, Service, SiteSettings, ContactMessage


@admin.register(Profile, site=admin_site)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin para el Perfil del desarrollador (Singleton).
    Solo se puede editar un perfil activo a la vez.
    """
    list_display = ('nombre', 'titulo_profesional', 'email', 'activo_badge')
    readonly_fields = ('fecha_actualizacion', 'preview_foto')
    
    fieldsets = (
        ('📱 Información Personal', {
            'fields': ('nombre', 'titulo_profesional', 'subtitulo_header', 'descripcion_corta')
        }),
        ('🖼️ Foto de Perfil', {
            'fields': ('foto_perfil', 'preview_foto'),
            'description': 'Sube una foto profesional en alta resolución'
        }),
        ('📝 Biografía', {
            'fields': ('bio', 'filosofia'),
            'classes': ('collapse',)
        }),
        ('💻 Tecnologías', {
            'fields': ('tecnologias',),
            'description': 'Separadas por coma: Python, Django, PostgreSQL, etc.'
        }),
        ('📧 Contacto', {
            'fields': ('email', 'telefono', 'ciudad', 'cv_url')
        }),
        ('🔗 Redes Sociales', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url'),
            'classes': ('collapse',)
        }),
        ('⚙️ Configuración', {
            'fields': ('mostrar_blog', 'mostrar_testimonios', 'activo'),
            'classes': ('collapse',)
        }),
        ('📊 Metadata', {
            'fields': ('fecha_actualizacion',),
            'classes': ('collapse',)
        }),
    )
    
    def activo_badge(self, obj):
        """Mostrar estado activo como badge"""
        if obj.activo:
            return format_html(
                '<span style="background-color:#28a745;color:white;padding:3px 10px;'
                'border-radius:3px;font-weight:bold;">{}</span>',
                '✓ ACTIVO'
            )
        return format_html(
            '<span style="background-color:#dc3545;color:white;padding:3px 10px;'
            'border-radius:3px;font-weight:bold;">{}</span>',
            '✗ INACTIVO'
        )
    activo_badge.short_description = 'Estado'
    
    def preview_foto(self, obj):
        """Preview de la foto de perfil"""
        if obj.foto_perfil:
            return format_html(
                '<img src="{}" width="150" height="150" '
                'style="border-radius:10px; border:2px solid #38bdf8;"/>',
                obj.foto_perfil.url
            )
        return 'Sin foto'
    preview_foto.short_description = 'Vista Previa'
    
    def has_add_permission(self, request):
        """Solo permitir un perfil"""
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """No permitir eliminar el perfil"""
        return False


@admin.register(Project, site=admin_site)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin para Proyectos con ordenamiento, búsqueda y filtros.
    """
    list_display = ('titulo', 'tecnologias', 'visible_badge', 'orden', 'fecha_creacion')
    list_filter = ('visible', 'fecha_creacion', 'tecnologias')
    search_fields = ('titulo', 'descripcion_corta', 'tecnologias')
    prepopulated_fields = {'slug': ('titulo',)}
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'preview_imagen')
    
    fieldsets = (
        ('📋 Información Básica', {
            'fields': ('titulo', 'slug', 'descripcion_corta', 'descripcion_completa')
        }),
        ('🖼️ Imagen', {
            'fields': ('imagen', 'preview_imagen'),
            'description': 'Dimensiones recomendadas: 800x600px'
        }),
        ('🔧 Tecnologías', {
            'fields': ('tecnologias',),
            'description': 'Separadas por coma: Django, PostgreSQL, Docker, etc.'
        }),
        ('🔗 Enlaces', {
            'fields': ('demo_url', 'github_url'),
            'classes': ('collapse',)
        }),
        ('⚙️ Configuración', {
            'fields': ('visible', 'orden')
        }),
        ('📊 Metadata', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )
    
    def visible_badge(self, obj):
        """Mostrar visibilidad como badge"""
        if obj.visible:
            return format_html(
                '<span style="background-color:#28a745;color:white;padding:3px 10px;'
                'border-radius:3px;">{}</span>',
                '👁️ Visible'
            )
        return format_html(
            '<span style="background-color:#6c757d;color:white;padding:3px 10px;'
            'border-radius:3px;">{}</span>',
            '🚫 Oculto'
        )
    visible_badge.short_description = 'Visibilidad'
    
    def preview_imagen(self, obj):
        """Preview de la imagen del proyecto"""
        if obj.imagen:
            return format_html(
                '<img src="{}" width="200" height="150" '
                'style="border-radius:5px; border:1px solid #38bdf8;"/>',
                obj.imagen.url
            )
        return 'Sin imagen'
    preview_imagen.short_description = 'Vista Previa'


@admin.register(Service, site=admin_site)
class ServiceAdmin(admin.ModelAdmin):
    """Admin para Servicios"""
    list_display = ('nombre', 'icono', 'visible_badge', 'orden')
    list_filter = ('visible', 'orden')
    search_fields = ('nombre', 'descripcion')
    
    fieldsets = (
        ('📝 Información', {
            'fields': ('nombre', 'descripcion', 'icono')
        }),
        ('⚙️ Configuración', {
            'fields': ('visible', 'orden')
        }),
    )
    
    def visible_badge(self, obj):
        """Mostrar visibilidad"""
        if obj.visible:
            return format_html(
                '<span style="background-color:#28a745;color:white;padding:3px 10px;'
                'border-radius:3px;">{}</span>',
                '✓ Visible'
            )
        return format_html(
            '<span style="background-color:#6c757d;color:white;padding:3px 10px;'
            'border-radius:3px;">{}</span>',
            '✗ Oculto'
        )
    visible_badge.short_description = 'Estado'


@admin.register(SiteSettings, site=admin_site)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Admin para Configuración Global del Sitio (Singleton).
    """
    list_display = ('titulo_sitio', 'actualizado')
    readonly_fields = ('actualizado',)
    
    fieldsets = (
        ('🌐 SEO y Metadata', {
            'fields': ('titulo_sitio', 'descripcion_sitio')
        }),
        ('📚 Secciones', {
            'fields': (
                'titulo_seccion_proyectos',
                'descripcion_seccion_proyectos',
                'titulo_seccion_servicios',
                'descripcion_seccion_servicios',
            )
        }),
        ('🦶 Footer', {
            'fields': ('texto_footer',),
            'classes': ('collapse',)
        }),
        ('👁️ Visibilidad de Secciones', {
            'fields': ('mostrar_projects', 'mostrar_services', 'mostrar_contact')
        }),
        ('📊 Analytics', {
            'fields': ('google_analytics_id',),
            'classes': ('collapse',)
        }),
        ('📅 Metadata', {
            'fields': ('actualizado',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Solo permitir una configuración"""
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """No permitir eliminar configuración"""
        return False


@admin.register(ContactMessage, site=admin_site)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin para Mensajes de Contacto.
    """
    list_display = ('name', 'email', 'subject', 'leido', 'created_at')
    list_filter = ('leido', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'email', 'name')
    
    fieldsets = (
        ('👤 De', {
            'fields': ('name', 'email')
        }),
        ('📬 Mensaje', {
            'fields': ('subject', 'message')
        }),
        ('✅ Estado', {
            'fields': ('leido',)
        }),
        ('📅 Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    list_editable = ('leido',)
    
    def has_add_permission(self, request):
        """No permitir crear mensajes desde admin"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Permitir eliminar solo para administradores"""
        return request.user.is_superuser
