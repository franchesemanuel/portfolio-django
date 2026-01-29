# 🎨 GUÍA DE ESTILOS CSS - Portfolio Premium

## 📊 Estructura CSS

El archivo `static/portfolio/css/style.css` está organizado en secciones claras:

```
✅ Variables de Color (:root)
✅ Tipografía (Poppins)
✅ Reset Global (*, html, body)
✅ Navbar
✅ Hero Section
✅ Botones
✅ Cards
✅ Secciones (About, Skills)
✅ Iconos
✅ Footer
✅ Animaciones
✅ Utilidades
✅ Formularios
✅ Responsive
```

---

## 🎨 VARIABLES CSS (Líneas 8-20)

### Colores Primarios
```css
--primary-dark: #0f172a;      /* Azul oscuro elegante */
--primary-darker: #0a0f1e;    /* Aún más oscuro */
```

### Colores Acentos
```css
--accent-cyan: #38bdf8;       /* Cian brillante */
--accent-blue: #0ea5e9;       /* Azul cielo */
```

### Colores de Texto
```css
--text-primary: #0f172a;      /* Texto oscuro */
--text-secondary: #475569;    /* Texto gris */
```

### Fondos
```css
--bg-light: #f8fafc;          /* Fondo muy claro */
--bg-white: #ffffff;          /* Blanco puro */
```

### Bordes
```css
--border-soft: #e2e8f0;       /* Bordes delicados */
```

### Sombras
```css
--shadow-soft: 0 4px 6px rgba(15, 23, 42, 0.07);
--shadow-medium: 0 10px 25px rgba(15, 23, 42, 0.1);
--shadow-large: 0 20px 40px rgba(15, 23, 42, 0.12);
```

---

## 🔤 TIPOGRAFÍA

### Fuente Principal
```css
font-family: 'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Importada de Google Fonts
```css
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
```

### Pesos Disponibles
- **300**: Light (títulos sutiles)
- **400**: Regular (texto normal)
- **500**: Medium (énfasis)
- **600**: Semibold (títulos)
- **700**: Bold (títulos principales)

### Ejemplos de Uso
```css
h1 { font-weight: 700; }      /* Bold */
h2 { font-weight: 700; }      /* Bold */
h3 { font-weight: 600; }      /* Semibold */
body { font-weight: 400; }    /* Regular */
.light { font-weight: 300; }  /* Light */
```

---

## 🔧 SISTEMA DE EASING (Transiciones)

### Easing Estándar Usado
```css
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
```

### Explicación
- **0.3s**: Duración (suave pero notoria)
- **cubic-bezier(0.4, 0, 0.2, 1)**: Curva profesional
  - Empieza rápido
  - Termina lento
  - Muy natural y elegante

---

## 🎯 NAVBAR (Líneas ~45-80)

### Fondo
```css
background: var(--primary-dark) !important;
box-shadow: var(--shadow-soft);
```

### Logo
```css
.navbar-brand {
    color: var(--bg-white) !important;
    font-weight: 700;
    font-size: 1.4rem;
    transition: color 0.3s ease;
}

.navbar-brand:hover {
    color: var(--accent-cyan) !important;
}
```

### Links de Navegación
```css
.nav-link {
    color: #cbd5e1 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.nav-link:hover {
    color: var(--accent-cyan) !important;
}

.nav-link::after {
    /* Underline animado en hover */
    content: '';
    width: 0;
    height: 2px;
    background: var(--accent-cyan);
    transition: width 0.3s;
}

.nav-link:hover::after {
    width: calc(100% - 3rem);
}
```

---

## 🌟 HERO SECTION (Líneas ~85-145)

### Contenedor
```css
.hero {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-darker) 100%);
    padding: 140px 0;
    position: relative;
    overflow: hidden;
}
```

### Efectos de Fondo
```css
.hero::before {
    /* Luz sutil cian + azul */
    background: 
        radial-gradient(circle at 20% 80%, rgba(56, 189, 248, 0.08) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(14, 165, 233, 0.08) 0%, transparent 50%);
}

.hero::after {
    /* Patrón grid sutil */
    background: url('data:image/svg+xml,...');
}
```

### Tipografía
```css
.hero h1 {
    font-size: clamp(2.5rem, 8vw, 4rem);  /* Fluida */
    font-weight: 700;
    margin-bottom: 1.5rem;
    letter-spacing: -1px;
    line-height: 1.2;
}

.hero p {
    font-size: clamp(1rem, 2vw, 1.25rem);
    color: #cbd5e1;
    font-weight: 300;
    line-height: 1.8;
}
```

---

## 💳 CARDS (Líneas ~150-195)

### Contenedor
```css
.card {
    border: 1px solid var(--border-soft);
    border-radius: 12px;
    box-shadow: var(--shadow-soft);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
    position: relative;
}
```

### Línea Decorativa Superior
```css
.card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-blue) 0%, var(--accent-cyan) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
}
```

### Hover
```css
.card:hover {
    transform: translateY(-8px);        /* Elevación */
    box-shadow: var(--shadow-large);    /* Sombra mayor */
    border-color: var(--accent-cyan);   /* Borde cian */
}

.card:hover::before {
    opacity: 1;  /* Línea aparece */
}
```

### Contenido
```css
.card-body {
    padding: 2rem;
}

.card-title {
    color: var(--primary-dark);
    font-weight: 600;
    margin-bottom: 1.2rem;
    font-size: 1.25rem;
}

.card-text {
    color: var(--text-secondary);
    line-height: 1.8;
}
```

---

## 🔘 BOTONES (Líneas ~197-240)

### Botón Primario
```css
.btn-primary {
    background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-cyan) 100%);
    border: none;
    padding: 12px 32px;
    font-weight: 600;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(14, 165, 233, 0.25);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 0.95rem;
    color: var(--bg-white) !important;
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(14, 165, 233, 0.35);
}

.btn-primary:active {
    transform: translateY(-1px);
}
```

### Botón Light
```css
.btn-light {
    background: rgba(248, 250, 252, 0.95) !important;
    color: var(--primary-dark) !important;
    font-weight: 600;
    border: 2px solid var(--bg-white);
}

.btn-light:hover {
    background: var(--bg-white) !important;
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
}
```

### Botón Outline
```css
.btn-outline-primary {
    color: var(--accent-blue);
    border: 2px solid var(--accent-blue);
}

.btn-outline-primary:hover {
    background: var(--accent-blue);
    color: var(--bg-white);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.25);
}
```

---

## 🎬 ANIMACIONES (Líneas ~470-505)

### Fade-In
```css
.fade-in {
    animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    opacity: 0;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(25px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
```

### Staggered Delays (Cards con Orden)
```css
.col-md-4:nth-child(1) .card { animation-delay: 0.1s; }
.col-md-4:nth-child(2) .card { animation-delay: 0.2s; }
.col-md-4:nth-child(3) .card { animation-delay: 0.3s; }
```

---

## 📱 RESPONSIVE (Líneas ~540-600+)

### Breakpoint 992px (Desktop Pequeño)
```css
@media (max-width: 992px) {
    .navbar-nav .nav-link {
        margin-left: 0;
        padding: 0.5rem 0;
    }
}
```

### Breakpoint 768px (Tablet)
```css
@media (max-width: 768px) {
    .hero {
        padding: 80px 0;
    }

    .hero h1 {
        font-size: 2.2rem;
    }

    .about-section {
        padding: 2rem 1.5rem;
    }

    .card-body {
        padding: 1.5rem;
    }
}
```

### Breakpoint 576px (Móvil)
```css
@media (max-width: 576px) {
    .hero {
        padding: 60px 0;
    }

    .hero h1 {
        font-size: 1.75rem;
    }

    .container {
        padding: 0 1rem;
    }

    .about-section {
        padding: 1.5rem 1rem;
    }

    h1 { font-size: 1.5rem; }
    h2 { font-size: 1.3rem; }
}
```

---

## 🔍 CÓMO PERSONALIZAR

### Cambiar Color Principal Globalmente
```css
:root {
    --primary-dark: #tu-color-aqui;  /* Cambia todo de una vez */
}
```

### Cambiar Velocidad de Transiciones
```css
/* Aumenta 0.3s a 0.5s para más lentitud */
transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
```

### Cambiar Easing
```css
/* De profesional a más rebotador */
cubic-bezier(0.68, -0.55, 0.265, 1.55)
```

### Aumentar/Disminuir Sombras
```css
--shadow-large: 0 30px 50px rgba(15, 23, 42, 0.2);  /* Más dramático */
```

---

## 🎯 MEJORES PRÁCTICAS USADAS

1. **Variables CSS** → Fácil mantenimiento
2. **Easing profesional** → Animaciones naturales
3. **Mobile-first** → Empieza pequeño, crece
4. **Flexbox/Grid** → Layouts flexibles
5. **clamp()** → Tipografía fluida
6. **Pseudoelementos** → Efectos sin HTML extra
7. **Transiciones suaves** → Experiencia premium
8. **Colores limitados** → Coherencia visual
9. **Espaciados consistentes** → Profesionalismo
10. **Accesibilidad** → Contraste suficiente

---

## 📊 COMPARATIVA ANTES/DESPUÉS

| Aspecto | Antes | Después |
|---------|-------|---------|
| **Líneas CSS** | ~90 | ~600 |
| **Colores** | Random | 8 variables |
| **Tipografía** | Sistema | Poppins |
| **Animaciones** | Ninguna | Fade-in, hover |
| **Cards** | Básicas | Premium |
| **Responsive** | Limitado | Mobile-first |
| **Profesionalismo** | Básico | Premium |

---

## 🚀 TIPS DE PERFORMANCE

1. **Las variables CSS se cachean** → Cambios rápidos
2. **Sin JavaScript innecesario** → Carga rápida
3. **Las imágenes escalables** → Menos datos
4. **Animaciones GPU** → transform y opacity
5. **Media queries eficientes** → Bien organizadas

---

**¡Tu CSS está listo para la producción!** ✨
