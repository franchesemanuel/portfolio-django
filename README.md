# Portfolio en Django

Este es un proyecto de portfolio profesional creado con Django y Bootstrap 5.

## Características

- Diseño responsivo con Bootstrap 5
- Secciones: Inicio, Sobre Mí, Proyectos, Contacto
- Estilos personalizados
- Navegación moderna

## Instalación

1. Clona o descarga el proyecto.
2. Crea un entorno virtual: `python -m venv .venv`
3. Activa el entorno: `source .venv/bin/activate` (macOS/Linux)
4. Instala dependencias: `pip install django`
5. Ejecuta migraciones: `python manage.py migrate`
6. Ejecuta el servidor: `python manage.py runserver`

## Personalización

- Edita los templates en `portfolio/templates/portfolio/`
- Agrega tu foto en `static/portfolio/images/profile.jpg`
- Modifica estilos en `static/portfolio/css/style.css`
- Actualiza contenido en las vistas

## Uso

Visita http://127.0.0.1:8000/ para ver el portfolio.