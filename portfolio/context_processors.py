"""
Context Processors para disponibilidad global de datos del CMS.
Los datos estarán disponibles en todos los templates automáticamente.
"""

from .models import Profile, SiteSettings


def cms_context(request):
    """
    Proporciona datos del CMS a todos los templates.
    
    Variables disponibles en templates:
    - profile: Datos del perfil del desarrollador
    - settings: Configuración general del sitio
    - projects_enabled: ¿Mostrar proyectos?
    - services_enabled: ¿Mostrar servicios?
    - contact_enabled: ¿Mostrar formulario de contacto?
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
