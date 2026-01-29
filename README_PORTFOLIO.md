# 🚀 GUÍA DE USO - Portfolio Django Premium

## ✅ ¿Qué cambió?

Tu portfolio ha sido completamente transformado de un diseño básico a un **portfolio premium profesional** apto para conseguir clientes o trabajo remoto.

---

## 📦 CÓMO EMPEZAR

### 1️⃣ Instalar Dependencias (Primera Vez)
```bash
cd /Users/francoemanuelsalcedo/Desktop/porfolio
pip install -r requirements.txt
```

### 2️⃣ Aplicar Migraciones (Primera Vez)
```bash
python3 manage.py migrate
```

### 3️⃣ Iniciar el Servidor
```bash
python3 manage.py runserver
```

### 4️⃣ Acceder al Portfolio
Abre el navegador en: **http://localhost:8000**

---

## 🎨 CAMBIOS VISUALES PRINCIPALES

### ✨ Colores Nuevos
- **Azul oscuro profesional**: #0f172a
- **Cian claro accent**: #38bdf8
- **Grises neutrales**: #475569, #e2e8f0
- **Blanco puro**: #ffffff

### 🔤 Tipografía
- **Fuente**: Poppins (moderna y profesional)
- **Importada automáticamente** de Google Fonts

### 🎯 Navbar
- Ahora es **sticky** (se mantiene visible al scroll)
- Logo con icono integrado
- Links con animación de underline en hover

### 🌟 Hero Section
- Rediseñado completamente
- Gradiente profesional oscuro
- Subtítulo y descripción mejorada
- Botón CTA más claro

### 💳 Cards
- Línea decorativa superior en hover
- Elevación suave (-8px)
- Sombras sofisticadas
- Bordes redondeados suaves

### 🔘 Botones
- Gradiente azul-cian
- Animaciones suaves
- Estados hover y active diferenciados

### 📱 Responsive
- Funciona perfecto en móvil, tablet, desktop
- Tipografía fluida
- Espaciados adaptables

---

## 📄 ARCHIVOS PRINCIPALES MODIFICADOS

### CSS
**`static/portfolio/css/style.css`**
- ~600 líneas completamente reescritas
- Variables CSS profesionales
- Animaciones suaves
- Responsive mobile-first

### Templates
1. **`portfolio/templates/portfolio/base.html`** - Base de todas las páginas
2. **`portfolio/templates/portfolio/home.html`** - Página de inicio
3. **`portfolio/templates/portfolio/about.html`** - Sobre mí
4. **`portfolio/templates/portfolio/projects.html`** - Proyectos
5. **`portfolio/templates/portfolio/contact.html`** - Contacto

### Python
1. **`portfolio/models.py`** - Agregado campo `subject`
2. **`portfolio/forms.py`** - Formulario actualizado
3. **`portfolio/migrations/0002_...py`** - Migración automática

---

## 🎨 PALETA DE COLORES DISPONIBLE

```css
:root {
    --primary-dark: #0f172a;        /* Azul oscuro principal */
    --primary-darker: #0a0f1e;      /* Más oscuro aún */
    --accent-cyan: #38bdf8;         /* Cian brillante */
    --accent-blue: #0ea5e9;         /* Azul cielo */
    --text-primary: #0f172a;        /* Texto oscuro */
    --text-secondary: #475569;      /* Texto gris */
    --bg-light: #f8fafc;            /* Fondo muy claro */
    --bg-white: #ffffff;            /* Blanco puro */
}
```

Si quieres cambiar colores, edita estas variables en `style.css` línea ~8.

---

## 🔧 CÓMO PERSONALIZAR

### 1. **Foto de Perfil**
Reemplaza:
```
portfolio/images/profile.jpg
```
Con tu propia foto (recomendado 250x250px cuadrada)

### 2. **Información de Contacto**
En `portfolio/templates/portfolio/contact.html` actualiza:
- Email: francoemanuelpp@gmail.com → tuEmail@ejemplo.com
- Teléfono: +34667221962 → tuTelefono
- Links a GitHub, LinkedIn, Twitter (línea ~65)

### 3. **Descripción de Proyectos**
En `portfolio/templates/portfolio/projects.html`:
- Edita títulos, descripciones, tecnologías
- Agrega links reales a "Ver Demo" y "GitHub"
- Personaliza íconos si lo deseas

### 4. **Sobre Mí**
En `portfolio/templates/portfolio/about.html`:
- Amplía tu descripción personal
- Actualiza habilidades
- Personaliza la filosofía de desarrollo

### 5. **Cambiar Colores Globales**
En `static/portfolio/css/style.css` línea 8:
```css
:root {
    --primary-dark: #tu-color;
    --accent-cyan: #tu-otro-color;
    /* etc */
}
```

---

## 📱 RESPONSIVE BREAKPOINTS

El diseño se adapta automáticamente:

| Pantalla | Breakpoint | Ajustes |
|----------|-----------|---------|
| Móvil | < 576px | Fuentes pequeñas, espacios reducidos |
| Tablet | 576px - 768px | Intermedios |
| Desktop | > 768px | Tamaño completo |
| Grande | > 992px | Máximo impacto |

---

## 🚀 DEPLOYMENT (Producción)

Cuando estés listo para publicar:

### Opción 1: Heroku
```bash
# Instala Heroku CLI
# Crea Procfile con: web: gunicorn portfolio_project.wsgi
# Agrega ALLOWED_HOSTS en settings.py
heroku create tuApp
heroku push heroku main
```

### Opción 2: PythonAnywhere
- Sube archivos vía FTP
- Configura virtual environment
- Actualiza WSGI file

### Opción 3: DigitalOcean / Linode
- VPS con Ubuntu
- Nginx + Gunicorn
- Certbot para SSL

**Importante**: 
- Configura `DEBUG = False` en producción
- Agrega HTTPS
- Usa ALLOWED_HOSTS correctamente
- Implementa collectstatic

---

## 🛠️ TROUBLESHOOTING

### Error: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Error: "Port 8000 already in use"
```bash
# Busca qué proceso está usando el puerto
lsof -i :8000

# Mata el proceso
kill -9 <PID>
```

### Migraciones no aplicadas
```bash
python3 manage.py migrate
```

### CSS no se actualiza
- Presiona Ctrl+Shift+R (hard refresh)
- O usa Cmd+Shift+R en Mac

---

## 📊 ESTRUCTURA DE CARPETAS

```
porfolio/
├── portfolio/                    # App Django principal
│   ├── templates/portfolio/
│   │   ├── base.html            # Template base
│   │   ├── home.html            # Página inicio
│   │   ├── about.html           # Sobre mí
│   │   ├── projects.html        # Proyectos
│   │   └── contact.html         # Contacto
│   ├── models.py                # ContactMessage (actualizado)
│   ├── forms.py                 # ContactForm (actualizado)
│   ├── views.py
│   └── urls.py
│
├── portfolio_project/           # Configuración Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/portfolio/
│   └── css/
│       └── style.css            # Estilos principales ⭐
│
├── manage.py                    # Django management
├── requirements.txt             # Dependencias
└── db.sqlite3                   # Base de datos
```

---

## 🎯 CHECKLIST POST-INSTALACIÓN

- [ ] Servidor ejecutándose: `python3 manage.py runserver`
- [ ] Página inicio carga: http://localhost:8000
- [ ] Foto de perfil visible en About
- [ ] Formulario funciona en Contact
- [ ] Links a navegación funcionan
- [ ] Diseño se ve bien en móvil (F12 → Responsive)
- [ ] Colores son los nuevos (azul oscuro + cian)
- [ ] Animaciones suaves funcionan
- [ ] Footer visible en todas las páginas

---

## 📚 DOCUMENTACIÓN RELACIONADA

- **TRANSFORMACION_COMPLETADA.md** - Detalle completo de cambios
- **CAMBIOS_DISEÑO.md** - Aspecto técnico de CSS

---

## ✨ TIPS PROFESIONALES

### 1. **Mantén el Código Limpio**
- Usa VSCode con Prettier para formatear
- Mantén variables CSS organizadas
- Comenta cambios importantes

### 2. **Performance**
- Optimiza imágenes (máximo 100KB)
- Usa lazy loading en imágenes
- Minifica CSS en producción

### 3. **Seguridad**
- Mantén Django actualizado
- Usa HTTPS en producción
- Valida siempre inputs del usuario
- Implementa rate limiting en formularios

### 4. **SEO**
- Agrega meta descriptions
- Usa heading tags correctamente
- Incluye alt text en imágenes
- Estructura HTML semántica (ya hecho ✅)

### 5. **Analytics**
- Agrega Google Analytics
- Monitorea conversiones de contacto
- Analiza dónde vienen los visitantes

---

## 🎉 ¡LISTO!

Tu portfolio está completamente configurado y listo para:
- ✅ Conseguir clientes
- ✅ Buscar trabajo remoto
- ✅ Participar en entrevistas
- ✅ Networking profesional

**¡A por esos proyectos!** 🚀

---

*Portfolio creado: 29 de Enero de 2026*
*Última actualización: Hoy*
