# 🏗️ ARQUITECTURA TÉCNICA - PORTFOLIO CMS

## 📋 TABLA DE CONTENIDOS
1. [Arquitectura General](#arquitectura-general)
2. [Modelos de Datos](#modelos-de-datos)
3. [Context Processors](#context-processors)
4. [Vistas](#vistas)
5. [Admin Personalizado](#admin-personalizado)
6. [Instrucciones de Desarrollo](#instrucciones-de-desarrollo)

---

## 🏗️ ARQUITECTURA GENERAL

### Patrón de Diseño
El portfolio implementa un **CMS dinámico** con los siguientes principios:

1. **Singleton Pattern** para Profile y SiteSettings
   - Solo una instancia activa en BD
   - Accesibles globalmente vía `get_active()` o `get_settings()`

2. **Context Processors** para disponibilidad global
   - Datos disponibles en **todos** los templates automáticamente
   - Sin necesidad de pasar en cada vista

3. **Template-driven** para flexibilidad
   - Todo cambio de contenido requiere solo BD, no código
   - Los templates cargan datos dinámicamente

### Stack Tecnológico
```
Django 6.0.1
├── ORM (django.db.models)
├── Admin (django.contrib.admin)
├── Forms (django.forms)
└── Templates (Jinja2)

Frontend
├── Bootstrap 5.3.0 (Grid + utilidades)
├── Poppins (Google Fonts)
└── FontAwesome 6.4.0 (Iconografía)

Base de Datos
└── SQLite3 (desarrollo)
```

---

## 📊 MODELOS DE DATOS

### 1. Profile (Singleton)

```python
class Profile(models.Model):
    # Información personal
    nombre: CharField
    titulo_profesional: CharField
    subtitulo_header: CharField
    
    # Media
    foto_perfil: ImageField  # Pillow required
    
    # Biografía
    bio: TextField
    filosofia: TextField
    descripcion_corta: CharField
    
    # Profesional
    tecnologias: TextField  # CSV format
    
    # Contacto
    email: EmailField
    telefono: CharField
    ciudad: CharField
    
    # Social
    github_url: URLField
    linkedin_url: URLField
    twitter_url: URLField
    cv_url: URLField
    
    # Configuración
    mostrar_blog: BooleanField
    mostrar_testimonios: BooleanField
    activo: BooleanField  # Singleton
    
    @classmethod
    def get_active(cls) -> Profile:
        """Obtener perfil activo (lazy creation)"""
        profile, created = cls.objects.get_or_create(
            activo=True,
            defaults=PROFILE_DEFAULTS
        )
        return profile
```

**Singleton Implementation:**
- Solo una instancia puede tener `activo=True`
- Override de `save()` desactiva otros
- `get_or_create` con defaults para inicialización

---

### 2. Project (Ordenado, Filtrable)

```python
class Project(models.Model):
    # Contenido
    titulo: CharField  # unique=False (permite duplicados)
    slug: SlugField    # unique=True (generado automáticamente)
    descripcion_corta: CharField
    descripcion_completa: TextField  # Opcional
    
    # Media
    imagen: ImageField  # 800x600px recomendado
    
    # Técnico
    tecnologias: CharField  # CSV: "Django, PostgreSQL, Docker"
    
    # Enlaces
    demo_url: URLField  # Opcional
    github_url: URLField  # Opcional
    
    # Ordenamiento
    orden: PositiveIntegerField  # 0=primero
    visible: BooleanField
    
    class Meta:
        ordering = ['orden', '-fecha_creacion']
    
    def get_tecnologias_list(self) -> list:
        """Convierte CSV a lista para template"""
        return [t.strip() for t in self.tecnologias.split(',')]
```

**Características:**
- Slug auto-generado por prepopulated_fields
- Ordenamiento dual: primero por `orden`, luego por fecha
- Método helper para procesar CSV en templates
- Filtrable por visible/fecha

---

### 3. Service (Soporte con Iconos)

```python
class Service(models.Model):
    # Contenido
    nombre: CharField
    descripcion: TextField
    
    # Presentación
    icono: CharField  # FontAwesome: "fas fa-code"
    
    # Configuración
    orden: PositiveIntegerField
    visible: BooleanField
    
    class Meta:
        ordering = ['orden', 'nombre']
```

**Iconos soportados:** FontAwesome 6.4.0+
```
fas fa-code, fas fa-shield-alt, fas fa-database, etc.
```

---

### 4. SiteSettings (Singleton)

```python
class SiteSettings(models.Model):
    # SEO
    titulo_sitio: CharField
    descripcion_sitio: CharField
    
    # Textos dinámicos
    titulo_seccion_proyectos: CharField
    descripcion_seccion_proyectos: TextField
    titulo_seccion_servicios: CharField
    descripcion_seccion_servicios: TextField
    texto_footer: TextField
    
    # Visibilidad
    mostrar_projects: BooleanField
    mostrar_services: BooleanField
    mostrar_contact: BooleanField
    
    # Analytics (opcional)
    google_analytics_id: CharField
    
    @classmethod
    def get_settings(cls) -> 'SiteSettings':
        """Obtener configuración activa (pk=1)"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
```

**Patrón Singleton con pk=1:**
- Solo una fila en BD (pk=1)
- `get_or_create` auto-crea con defaults
- Sin necesidad de custom manager

---

### 5. ContactMessage

```python
class ContactMessage(models.Model):
    # Remitente
    name: CharField
    email: EmailField
    
    # Contenido
    subject: CharField
    message: TextField
    
    # Metadata
    leido: BooleanField  # ✓ Nuevo
    created_at: DateTimeField  # auto_now_add
    
    class Meta:
        ordering = ['-created_at']
```

**Cambios respecto original:**
- Agregado campo `leido` para seguimiento
- Ordenamiento por fecha descendente

---

## 🔌 CONTEXT PROCESSORS

### Ubicación
```
portfolio/context_processors.py
```

### Función Principal

```python
def cms_context(request):
    """
    Proporciona contexto global CMS a todos los templates.
    
    Variables disponibles:
    - profile: Profile activo
    - settings: SiteSettings activo
    - projects_enabled: bool
    - services_enabled: bool
    - contact_enabled: bool
    """
    profile = Profile.get_active()
    site_settings = SiteSettings.get_settings()
    
    return {
        'profile': profile,
        'settings': site_settings,
        'projects_enabled': site_settings.mostrar_projects,
        'services_enabled': site_settings.mostrar_services,
        'contact_enabled': site_settings.mostrar_contact,
    }
```

### Registración en settings.py

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # Django defaults...
                'portfolio.context_processors.cms_context',  # ← Agregar aquí
            ],
        },
    },
]
```

### Disponibilidad en Templates

```django
{{ profile.nombre }}              {# Franco Emanuel Salcedo #}
{{ settings.titulo_sitio }}       {# Franco Emanuel - Portfolio #}
{% if projects_enabled %}...{% endif %}
```

---

## 👀 VISTAS

Todas las vistas cargan datos dinámicamente:

### home(request)
```python
def home(request):
    context = {
        'profile': Profile.get_active(),
        'settings': SiteSettings.get_settings(),
        'featured_projects': Project.objects.filter(visible=True)[:3],
    }
    return render(request, 'portfolio/home.html', context)
```
**Datos:** Profile, Settings, 3 primeros proyectos visibles

---

### about(request)
```python
def about(request):
    profile = Profile.get_active()
    services = Service.objects.filter(visible=True)
    
    # Procesar CSV de tecnologías
    tecnologias = [t.strip() for t in profile.tecnologias.split(',')]
    
    context = {
        'profile': profile,
        'settings': SiteSettings.get_settings(),
        'services': services,
        'tecnologias': tecnologias,
    }
    return render(request, 'portfolio/about.html', context)
```
**Datos:** Profile, Settings, Servicios, Tecnologías como lista

---

### projects(request)
```python
def projects(request):
    projects_list = Project.objects.filter(visible=True)\
        .order_by('orden', '-fecha_creacion')
    
    context = {
        'projects': projects_list,
        'profile': Profile.get_active(),
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'portfolio/projects.html', context)
```
**Datos:** Todos los proyectos visibles, ordenados

---

### contact(request)
```python
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # ContactMessage en BD
            messages.success(request, '¡Mensaje enviado!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'profile': Profile.get_active(),
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'portfolio/contact.html', context)
```
**Datos:** Profile, Settings, Formulario

---

## 🎛️ ADMIN PERSONALIZADO

### ProfileAdmin (Singleton Management)

```python
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = (
        ('📱 Información Personal', {
            'fields': ('nombre', 'titulo_profesional', 'subtitulo_header')
        }),
        ('🖼️ Foto de Perfil', {
            'fields': ('foto_perfil', 'preview_foto'),
        }),
        ('💻 Tecnologías', {
            'fields': ('tecnologias',),
            'description': 'Separadas por coma'
        }),
        ('🔗 Redes Sociales', {
            'fields': ('github_url', 'linkedin_url', 'twitter_url'),
        }),
    )
    
    def has_add_permission(self, request):
        """Solo permitir 1 perfil"""
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """No permitir borrar"""
        return False
```

**Características:**
- Fieldsets organizados con emojis
- Preview de imagen en tiempo real
- Prevención de múltiples instancias
- Protección contra eliminación

---

### ProjectAdmin (CRUD Completo)

```python
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tecnologias', 'visible_badge', 'orden')
    list_filter = ('visible', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion_corta')
    prepopulated_fields = {'slug': ('titulo',)}  # Auto slug
    readonly_fields = ('fecha_creacion', 'preview_imagen')
    
    fieldsets = (
        ('📋 Información', {
            'fields': ('titulo', 'slug', 'descripcion_corta')
        }),
        ('🖼️ Imagen', {
            'fields': ('imagen', 'preview_imagen'),
        }),
        ('🔗 Enlaces', {
            'fields': ('demo_url', 'github_url'),
        }),
        ('⚙️ Configuración', {
            'fields': ('visible', 'orden'),
        }),
    )
```

**Características:**
- Slugs auto-generados
- Vista previa de imágenes
- Filtros por visibility y fecha
- Búsqueda full-text

---

### SiteSettingsAdmin (Global Config)

```python
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🌐 SEO', {
            'fields': ('titulo_sitio', 'descripcion_sitio'),
        }),
        ('👁️ Visibilidad', {
            'fields': ('mostrar_projects', 'mostrar_services', 'mostrar_contact'),
        }),
    )
    
    def has_add_permission(self, request):
        """Solo 1 configuración"""
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
```

---

## 🚀 INSTRUCCIONES DE DESARROLLO

### Instalación Inicial

```bash
# 1. Entrar a venv
cd /Users/francoemanuelsalcedo/Desktop/porfolio
source .venv/bin/activate

# 2. Instalar dependencias (si falta algo)
pip install Pillow
pip install Django==6.0.1

# 3. Aplicar migraciones
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 5. Iniciar servidor
python manage.py runserver 8000

# 6. Acceder
# http://localhost:8000/admin/
```

### Makemigrations (Cambios en Models)

```bash
# Si cambias algo en models.py
python manage.py makemigrations portfolio

# Revisa el archivo generado
cat portfolio/migrations/000X_*.py

# Aplica
python manage.py migrate
```

### Shell Django (Debugging)

```bash
python manage.py shell

# Dentro del shell:
from portfolio.models import Profile, Project
p = Profile.get_active()
print(p.nombre)

projects = Project.objects.filter(visible=True)
for p in projects:
    print(f"{p.titulo}: {p.tecnologias}")
```

### Recolectar Static (Producción)

```bash
python manage.py collectstatic --noinput
```

### Crear Admin desde Shell

```bash
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@test.com', 'password123')
```

---

## 📝 CONVENCIONES DE CÓDIGO

### Nombres de Modelos
```python
class Profile(...)          # Singular, capital
class ContactMessage(...)   # Explicit, descriptive
```

### Nombres de Campos
```python
titulo_profesional    # snake_case
foto_perfil          # descriptivo
crear_at             # timestamp always
visible              # boolean default True
orden                # positive int default 0
```

### Métodos de Clase
```python
@classmethod
def get_active(cls):       # getter para singletons
    ...

def get_tecnologias_list(self):  # procesar datos
    ...
```

### Variables en Templates
```django
{{ profile.nombre }}       # snake_case
{{ settings.titulo_sitio }}
{% if projects_enabled %}  # boolean flag
```

---

## 🔒 SEGURIDAD

### Implementado
- ✅ CSRF Protection (Django built-in)
- ✅ SQL Injection Protection (ORM)
- ✅ XSS Protection (Template escaping)
- ✅ Admin authentication
- ✅ Permission-based (superuser only)

### Recomendaciones Producción
```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🧪 TESTING

Estructura preparada para tests:

```python
# portfolio/tests.py
from django.test import TestCase
from .models import Profile, Project

class ProfileTestCase(TestCase):
    def setUp(self):
        self.profile = Profile.get_active()
    
    def test_singleton(self):
        """Solo una instancia activa"""
        p2 = Profile.objects.create(nombre='Test', activo=True)
        self.assertEqual(Profile.objects.filter(activo=True).count(), 1)
    
    def test_tecnologias_parsing(self):
        """CSV parsing correcto"""
        techs = self.profile.get_tecnologias_list()
        self.assertIsInstance(techs, list)
```

---

## 📊 MIGRACIONES

### Historia
```
0001_initial.py          ← ContactMessage original
0002_...py               ← Add subject field
0003_profile_project...  ← Modelos CMS completos
```

### Revertar Migración
```bash
python manage.py migrate portfolio 0001
# Vuelve a estado inicial (cuidado: borra data)
```

---

## 🎯 ENDPOINTS

| URL | Vista | Modelo |
|-----|-------|--------|
| `/` | home | Profile, Projects |
| `/about/` | about | Profile, Services |
| `/projects/` | projects | Projects |
| `/contact/` | contact | ContactMessage |
| `/admin/` | Django Admin | Todos |

---

## ✨ CARACTERÍSTICAS ESPECIALES

### Auto-slug en Projects
```python
prepopulated_fields = {'slug': ('titulo',)}
# Genera automáticamente slug desde título
```

### Image Preview en Admin
```python
def preview_imagen(self, obj):
    return format_html(f'<img src="{obj.imagen.url}" width="200">')
```

### Singleton Enforcement
```python
def save(self, *args, **kwargs):
    if self.activo:
        Profile.objects.filter(activo=True).exclude(pk=self.pk).update(activo=False)
    super().save(*args, **kwargs)
```

---

## 📚 REFERENCIAS

- [Django ORM](https://docs.djangoproject.com/en/6.0/topics/db/models/)
- [Django Admin](https://docs.djangoproject.com/en/6.0/ref/contrib/admin/)
- [Django Templates](https://docs.djangoproject.com/en/6.0/topics/templates/)
- [Pillow (Images)](https://pillow.readthedocs.io/)
- [FontAwesome Icons](https://fontawesome.com/icons)

---

**Documento técnico completo para desarrolladores y futuros mantenedores.**
