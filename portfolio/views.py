from django.shortcuts import render, redirect
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from .forms import ContactForm
from .models import Profile, Project, Service, SiteSettings


def home(request):
    """
    Vista Home - Carga datos dinámicos del CMS.
    """
    context = {
        'profile': Profile.get_active(),
        'settings': SiteSettings.get_settings(),
        'featured_projects': Project.objects.filter(visible=True)[:3],
    }
    return render(request, 'portfolio/home.html', context)


def about(request):
    """
    Vista About - Información del perfil desde CMS.
    """
    profile = Profile.get_active()
    services = Service.objects.filter(visible=True)
    
    # Convertir string de tecnologías a lista
    tecnologias = [t.strip() for t in profile.tecnologias.split(',')]
    
    context = {
        'profile': profile,
        'settings': SiteSettings.get_settings(),
        'services': services,
        'tecnologias': tecnologias,
    }
    return render(request, 'portfolio/about.html', context)


def projects(request):
    """
    Vista Projects - Listado dinámico de proyectos.
    """
    projects_list = Project.objects.filter(visible=True).order_by('orden', '-fecha_creacion')
    
    context = {
        'projects': projects_list,
        'profile': Profile.get_active(),
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'portfolio/projects.html', context)


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def contact(request):
    """
    Vista Contact - Formulario de contacto con datos dinámicos.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Mensaje enviado exitosamente! Te contactaré pronto.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    profile = Profile.get_active()
    context = {
        'form': form,
        'profile': profile,
        'settings': SiteSettings.get_settings(),
    }
    return render(request, 'portfolio/contact.html', context)
