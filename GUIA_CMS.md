# 🎯 GUÍA COMPLETA: PORTFOLIO PERSONALIZABLE CON CMS DJANGO

## 📋 Introducción

Tu portfolio se ha transformado en un **CMS completamente personalizable**. Ahora puedes cambiar casi todo el contenido **sin tocar código**, solo desde el Panel de Administración de Django.

**No más hardcode.** No más edición de HTML. Todo se gestiona desde la BD.

---

## 🚀 ACCESO AL ADMIN

### URL
```
http://localhost:8000/admin/
```

### Credenciales
```
Usuario: franchesemanuel
Contraseña: Savita1991
```

---

## 📊 MODELOS DEL CMS

### 1. **Profile** (Perfil del Desarrollador)
**Singleton** - Solo puede haber uno activo. Contiene toda tu información personal y profesional.

#### Campos principales:
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `nombre` | Texto | Nombre completo (aparece en navbar y hero) |
| `titulo_profesional` | Texto | Tu título (ej: "Desarrollador Senior") |
| `subtitulo_header` | Texto | Texto que aparece en el hero bajo el nombre |
| `foto_perfil` | Imagen | Foto que aparece en "Sobre mí" |
| `bio` | Texto largo | Biografía completa |
| `filosofia` | Texto largo | Tu filosofía de trabajo (blockquote) |
| `tecnologias` | Texto largo | Tecnologías separadas por coma |
| `email` | Email | Email de contacto |
| `telefono` | Texto | Teléfono con formato |
| `ciudad` | Texto | Tu ubicación |
| `github_url` | URL | Link a tu perfil de GitHub |
| `linkedin_url` | URL | Link a tu perfil de LinkedIn |
| `twitter_url` | URL | Link a tu perfil de Twitter |
| `cv_url` | URL | Link a tu CV descargable |

#### Cómo editar:
1. Entra al admin
2. Haz click en "Perfil del Desarrollador"
3. Edita los campos que necesites
4. **Importante:** La imagen debe ser JPG o PNG
5. Guarda cambios
6. ¡Los cambios aparecen al instante en la web!

---

### 2. **Project** (Proyectos)
Tus trabajos/proyectos. Puedes agregar **ilimitados** y ordenarlos por importancia.

#### Campos principales:
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `titulo` | Texto | Nombre del proyecto |
| `slug` | Slug | URL amigable (auto-generado) |
| `descripcion_corta` | Texto | Descripción de tarjeta |
| `descripcion_completa` | Texto largo | Descripción detallada (opcional) |
| `imagen` | Imagen | Screenshot del proyecto |
| `tecnologias` | Texto | Stack técnico (ej: Django, PostgreSQL, Docker) |
| `demo_url` | URL | Link al proyecto en vivo |
| `github_url` | URL | Link al repositorio |
| `orden` | Número | Orden de aparición (0 = primero) |
| `visible` | Booleano | ¿Mostrar en la web? |

#### Cómo agregar un proyecto:
1. Entra al admin
2. Haz click en "+ Agregar" en "Proyectos"
3. Completa la información
4. **Importante:** Las tecnologías van separadas por coma
5. Guarda y ¡listo! Aparece en `/projects/`

#### Ejemplo de tecnologías:
```
Django, PostgreSQL, Docker, GitHub Actions
```

---

### 3. **Service** (Servicios)
Los servicios que ofreces. Aparecen en "Sobre mí".

#### Campos:
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `nombre` | Texto | Nombre del servicio |
| `descripcion` | Texto largo | Qué incluye |
| `icono` | Texto | Icono FontAwesome (ej: fas fa-code) |
| `orden` | Número | Orden de aparición |
| `visible` | Booleano | ¿Mostrar? |

#### Iconos disponibles:
```
fas fa-code          (Código)
fas fa-shield-alt    (Seguridad)
fas fa-database      (Base de datos)
fas fa-plug          (APIs)
fas fa-lightbulb     (Ideas)
fas fa-rocket        (Proyectos)
fas fa-lock          (Seguridad)
fas fa-globe         (Web)
fas fa-wrench        (Configuración)
```

---

### 4. **SiteSettings** (Configuración Global)
**Singleton** - Configuración general del sitio. Solo una.

#### Campos principales:
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `titulo_sitio` | Texto | Título que aparece en navegador |
| `descripcion_sitio` | Texto | Meta description para SEO |
| `titulo_seccion_proyectos` | Texto | "Mis Proyectos" o tu título |
| `descripcion_seccion_proyectos` | Texto largo | Subtítulo de proyectos |
| `titulo_seccion_servicios` | Texto | "¿Qué Ofrezco?" o tu título |
| `texto_footer` | Texto largo | Copyright y info del footer |
| `mostrar_projects` | Booleano | ¿Mostrar sección de proyectos? |
| `mostrar_services` | Booleano | ¿Mostrar sección de servicios? |
| `mostrar_contact` | Booleano | ¿Mostrar formulario de contacto? |
| `google_analytics_id` | Texto | ID de Google Analytics (opcional) |

#### Cómo editar:
1. Entra al admin
2. Haz click en "Configuración del Sitio"
3. Edita lo que necesites
4. Las secciones se activan/desactivan con los checkboxes

---

### 5. **ContactMessage** (Mensajes de Contacto)
Los mensajes que reciben en el formulario. **Solo lectura desde admin** (no puedes crear).

#### Campos:
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `name` | Texto | Nombre de quien escribe |
| `email` | Email | Email de contacto |
| `subject` | Texto | Asunto del mensaje |
| `message` | Texto largo | El mensaje completo |
| `leido` | Booleano | ¿Ya lo leíste? |
| `created_at` | Fecha | Cuándo llegó |

#### Cómo usar:
1. Los mensajes llegan automáticamente al formulario
2. En el admin ves todos los mensajes
3. Marca como "Leído" para organizarte
4. Puedes filtrar por fecha o estado
5. Puedes eliminar mensajes antiguos (solo superusuario)

---

## 🔄 FLUJO DE DATOS: CÓMO FUNCIONA TODO

```
┌─────────────────────────────────────────────────────────────┐
│                    PANEL DE ADMIN                           │
│  ✎ Editas aquí: Profile, Projects, Services, Settings     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
            ┌──────────────┐
            │   BD (SQLite)│  ← Datos guardados
            └──────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────┐
│           CONTEXT PROCESSORS (Disponibilidad global)       │
│  • profile = datos del perfil actual                        │
│  • settings = configuración del sitio                       │
│  • projects_enabled = ¿Mostrar proyectos?                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────────────────┐
│                  TEMPLATES (HTML)                           │
│  • base.html         ← Navbar y footer dinámicos            │
│  • home.html         ← Hero con datos de profile            │
│  • about.html        ← Bio, tecnologías, servicios          │
│  • projects.html     ← Lista de proyectos dinámicos         │
│  • contact.html      ← Email y links de profile             │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
         ┌────────────────┐
         │ 🌐 NAVEGADOR   │  ← Tu web actualizada
         └────────────────┘
```

---

## 🎨 PERSONALIZACIÓN PASO A PASO

### 1️⃣ Cambiar tu Nombre y Título
```
Admin → Perfil del Desarrollador
✎ Nombre: Tu nombre real
✎ Título Profesional: Tu specialidad
✎ Subtítulo Header: Una frase impactante
```

### 2️⃣ Agregar tu Foto
```
Admin → Perfil del Desarrollador
⬆️ Foto de Perfil: Sube tu foto (JPG/PNG, mín 400x400px)
💡 Recomendación: Foto profesional, fondo neutro
```

### 3️⃣ Actualizar Redes Sociales
```
Admin → Perfil del Desarrollador
🔗 GitHub: https://github.com/tuuser
🔗 LinkedIn: https://linkedin.com/in/tuuser
🔗 Twitter: https://twitter.com/tuuser
💡 Los links aparecen en navbar y footer
```

### 4️⃣ Agregar Proyectos
```
Admin → Proyectos → + Agregar
📋 Título: Mi Proyecto Increíble
📝 Descripción corta: Una línea impactante
🖼️ Imagen: Screenshot del proyecto
🔧 Tecnologías: Django, PostgreSQL, Docker
🔗 Demo URL: https://mi-proyecto.com
🔗 GitHub: https://github.com/user/proyecto
📌 Orden: 1 (primero), 2 (segundo), etc
👁️ Visible: ✓ (si está activo)
```

### 5️⃣ Cambiar Textos del Sitio
```
Admin → Configuración del Sitio
✎ Título Sitio: Para navegador y SEO
✎ Descripción: Meta description en Google
✎ Títulos de secciones: "Mis Trabajos", etc
✎ Footer: Copyright personalizado
```

### 6️⃣ Activar/Desactivar Secciones
```
Admin → Configuración del Sitio
☑️ Mostrar Proyectos: Checkear para ver/ocultar
☑️ Mostrar Servicios: Checkear para ver/ocultar
☑️ Mostrar Contacto: Checkear para ver/ocultar
```

---

## 📱 DONDE APARECEN LOS DATOS

### Profile (Perfil)
- **Navbar:** nombre
- **Home:** nombre, título, subtítulo
- **About:** nombre, foto, bio, filosofía, tecnologías
- **Contact:** email, teléfono, ciudad, redes sociales
- **Everywhere:** En el contexto global

### Projects (Proyectos)
- **Home:** 3 proyectos destacados
- **Projects:** Lista completa filtrada por visible=True
- **Ordenados:** Por campo `orden`

### Services (Servicios)
- **About:** Lista de servicios con iconos
- **Solo si visible=True**
- **Ordenados:** Por campo `orden`

### SiteSettings (Configuración)
- **Head:** Título y meta description
- **Footer:** Texto del pie
- **Navbar:** Proyecto visible en menú
- **Global:** Controla qué secciones se muestran

---

## 🔐 SEGURIDAD Y BUENAS PRÁCTICAS

### ✅ Haz esto:
- Guarda tus URLs reales (GitHub, LinkedIn)
- Usa fotos profesionales
- Actualiza la descripción periódicamente
- Mantén los datos del perfil consistentes
- Usa contraseñas fuertes para el admin

### ❌ Evita esto:
- Cambiar el nombre de campos en modelos (rompe todo)
- Borrar el Profile o SiteSettings
- Subir imágenes muy grandes (ralentizan)
- Incluir HTML en los campos de texto

---

## 🔧 CAMPOS ESPECÍFICOS IMPORTANTES

### `slug` en Proyectos
**No lo edites una vez guardado.** Se genera automáticamente del título.

### `orden` en Proyectos y Servicios
- Números **menores aparecen primero**
- 0, 1, 2, 3... (no necesitan ser consecutivos)
- Proyectos con mismo `orden` se ordenan por fecha

### `visible` (Proyectos y Servicios)
- ✓ Checked = Aparece en la web
- ☐ Unchecked = Oculto (no aparece pero está guardado)

### `tecnologias` en Profile y Projects
Separa por **coma**:
```
Django, PostgreSQL, Docker, Kubernetes, GitHub Actions
```
Se mostrarán como **badges** en proyectos

### Icono en Servicios
Usa **nombres de FontAwesome 6.4.0**:
```
fas fa-code
fas fa-shield-alt
fas fa-database
far fa-star         ← También "far" o "fab"
fab fa-github
```
[Busca aquí](https://fontawesome.com/icons) los que quieras

---

## 📈 ESTADÍSTICAS Y METADATA

- **Profile:** Fecha de última actualización
- **Projects:** Fecha de creación y actualización
- **ContactMessage:** Fecha de recepción
- **SiteSettings:** Última actualización

Todo se llena automáticamente, no necesitas hacerlo.

---

## 🚀 CASOS DE USO

### Cambiar email de contacto
```
Admin → Perfil → email: tuemail@nuevo.com
Guarda → ¡Aparece en Contact y footer!
```

### Ocultar temporalmente proyectos
```
Admin → Proyectos → [proyecto] → visible: ☐
Guarda → ¡Se oculta de la web!
```

### Cambiar orden de proyectos
```
Admin → Proyectos
Proyecto 1: orden = 1 (primero)
Proyecto 2: orden = 2 (segundo)
Proyecto 3: orden = 3 (tercero)
Guarda → ¡Se reordenan automáticamente!
```

### Personalizar cada sección
```
Admin → Configuración del Sitio
Cambias títulos y descripciones de secciones
Guarda → ¡Aparecen en cada página!
```

---

## 🎓 TIPS PROFESIONALES

1. **Fotos:** Usa imágenes de alta calidad (min 800x600px para proyectos)
2. **Descripciones:** Sé específico y detallado
3. **URLs:** Asegúrate que todos los links funcionan
4. **SEO:** La descripción del sitio aparece en Google
5. **Mobile:** El portafolio es responsive, probado en todos tamaños
6. **Actualizaciones:** Actualiza proyectos regularmente
7. **Mensajes:** Revisa regularmente los mensajes de contacto

---

## 🐛 TROUBLESHOOTING

### "La imagen no sube"
→ Asegúrate que sea JPG o PNG
→ Máximo recomendado: 5MB
→ Dimensiones: mín 400x400px

### "No veo los cambios en la web"
→ Recarga la página (Ctrl+F5 o Cmd+Shift+R)
→ Limpia caché del navegador
→ El servidor debe estar corriendo

### "El slug se generó mal"
→ No importa, puedes ignorarlo
→ Solo afecta URLs internas

### "Quiero cambiar el CSS"
→ El CSS está en `static/portfolio/css/style.css`
→ Puedes editarlo, pero no es necesario para cambiar contenido
→ Los cambios se recargan automáticamente

### "¿Puedo cambiar el nombre de los campos?"
→ **NO.** Romperá la web
→ Los nombres de campos están en el código y templates
→ Solo cambia los **valores**, no los nombres

---

## 📚 ARCHIVOS IMPORTANTES

```
portfolio/
├── models.py              ← Definición de modelos (no tocar)
├── admin.py               ← Panel admin (no necesitas editar)
├── views.py               ← Lógica de vistas (dinámicas)
├── context_processors.py  ← Disponibilidad de datos
└── migrations/
    └── 0003_...py         ← Cambios de BD (no tocar)

templates/
├── base.html              ← Navbar y footer (dinámicos)
├── home.html              ← Hero (dinámico)
├── about.html             ← Bio y servicios (dinámicos)
├── projects.html          ← Lista de proyectos (dinámica)
└── contact.html           ← Contacto (dinámico)

static/
└── css/
    └── style.css          ← Estilos (puedes editar)
```

---

## ✨ RESUMEN FINAL

Tu portfolio es ahora un **CMS profesional**:

✅ **Contenido 100% personalizable** desde el admin
✅ **Sin necesidad de código** para cambiar información
✅ **Seguro:** Solo tú accedes al admin
✅ **Escalable:** Agrega proyectos ilimitados
✅ **Profesional:** Diseño moderno y responsivo
✅ **SEO ready:** Meta tags dinámicos
✅ **Mobile first:** Funciona perfecto en móvil

**¡Ahora es un producto real, listo para clientes!**

---

## 🤝 SOPORTE

Si necesitas ayuda:
1. Revisa este documento
2. Abre el navegador developer (F12)
3. Consulta logs en la terminal del servidor

¡Éxito con tu portfolio! 🚀
