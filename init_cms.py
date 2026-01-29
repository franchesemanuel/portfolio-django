#!/usr/bin/env python
"""
Script para inicializar los datos del CMS.
Ejecutar con: python init_cms.py
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from portfolio.models import Profile, SiteSettings, Service

def init_cms():
    """Inicializar datos del CMS"""
    
    print("=" * 80)
    print("🚀 INICIALIZANDO CMS DEL PORTFOLIO")
    print("=" * 80)
    
    # 1. Crear/Actualizar Profile
    print("\n📝 Configurando Perfil...")
    profile, created = Profile.objects.get_or_create(
        activo=True,
        defaults={
            'nombre': 'Franco Emanuel Salcedo',
            'titulo_profesional': 'Desarrollador Django + Especialista en Ciberseguridad',
            'subtitulo_header': 'Creo aplicaciones web seguras, escalables y profesionales, auditadas desde el primer día.',
            'descripcion_corta': 'Desarrollo web con seguridad integrada desde el primer día',
            'bio': 'Soy desarrollador web especializado en Django, con un enfoque integral en seguridad, calidad y buenas prácticas. Creo aplicaciones web funcionales, escalables y profesionales.',
            'filosofia': 'La seguridad no es un agregado, es un principio fundamental en el desarrollo.',
            'tecnologias': 'Django, Python, PostgreSQL, REST APIs, Docker, Linux, JavaScript, Bootstrap, Git',
            'email': 'franco@example.com',
            'telefono': '+34 600 000 000',
            'ciudad': 'España',
            'github_url': 'https://github.com/franchesemanuel',
            'linkedin_url': 'https://linkedin.com/in/franco',
        }
    )
    
    if created:
        print("✅ Perfil creado exitosamente")
    else:
        print("✓ Perfil ya existe")
    
    # 2. Crear/Actualizar SiteSettings
    print("\n⚙️  Configurando Sitio...")
    settings, created = SiteSettings.objects.get_or_create(
        pk=1,
        defaults={
            'titulo_sitio': 'Franco Emanuel - Desarrollador Django + Ciberseguridad',
            'descripcion_sitio': 'Portfolio profesional de desarrollador Django especializado en ciberseguridad',
            'titulo_seccion_proyectos': 'Mis Proyectos',
            'descripcion_seccion_proyectos': 'Proyectos que muestran mi expertise en desarrollo seguro y escalable',
            'titulo_seccion_servicios': '¿Qué Ofrezco?',
            'descripcion_seccion_servicios': 'Servicios profesionales para tu proyecto',
            'texto_footer': '© 2026 Franco Emanuel Salcedo. Todos los derechos reservados.',
            'mostrar_projects': True,
            'mostrar_services': True,
            'mostrar_contact': True,
        }
    )
    
    if created:
        print("✅ Configuración del sitio creada exitosamente")
    else:
        print("✓ Configuración del sitio ya existe")
    
    # 3. Crear Servicios si no existen
    print("\n🎯 Configurando Servicios...")
    
    services_data = [
        {
            'nombre': 'Desarrollo Web',
            'descripcion': 'Aplicaciones web modernas y escalables con Django',
            'icono': 'fas fa-code',
            'orden': 1,
        },
        {
            'nombre': 'APIs REST',
            'descripcion': 'APIs robustas y seguras con Django REST Framework',
            'icono': 'fas fa-plug',
            'orden': 2,
        },
        {
            'nombre': 'Auditoría de Seguridad',
            'descripcion': 'Análisis de vulnerabilidades y pruebas de penetración',
            'icono': 'fas fa-shield-alt',
            'orden': 3,
        },
        {
            'nombre': 'Consultoría Tech',
            'descripcion': 'Asesoramiento en arquitectura y mejores prácticas',
            'icono': 'fas fa-lightbulb',
            'orden': 4,
        },
    ]
    
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            nombre=service_data['nombre'],
            defaults=service_data
        )
        if created:
            print(f"  ✅ Servicio '{service_data['nombre']}' creado")
        else:
            print(f"  ✓ Servicio '{service_data['nombre']}' ya existe")
    
    print("\n" + "=" * 80)
    print("✨ ¡CMS INICIALIZADO EXITOSAMENTE!")
    print("=" * 80)
    print("\n📊 Datos de acceso al Admin:")
    print(f"   URL: http://127.0.0.1:8000/admin/")
    print(f"   Usuario: franchesemanuel")
    print(f"   Contraseña: Savita1991")
    print("\n💡 Próximos pasos:")
    print("   1. Accede al admin")
    print("   2. Edita tu Perfil (foto, email, links, etc)")
    print("   3. Agrega Proyectos")
    print("   4. Personaliza la Configuración del Sitio")
    print("   5. Visita http://127.0.0.1:8000/ para ver los cambios")
    print("=" * 80 + "\n")

if __name__ == '__main__':
    init_cms()
