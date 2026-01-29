# 🛠️ REFERENCIA RÁPIDA DE COMANDOS

## 🚀 Iniciar Servidor

```bash
cd /Users/francoemanuelsalcedo/Desktop/porfolio
source .venv/bin/activate
python manage.py runserver
```

Luego accede a: **http://localhost:8000/**

---

## 🔐 Acceso Admin

```
URL: http://localhost:8000/admin/
Usuario: franchesemanuel
Contraseña: Savita1991
```

---

## 🗄️ Comandos de Base de Datos

### Ver todas las migraciones
```bash
python manage.py showmigrations
```

### Crear nuevas migraciones (después de cambiar models.py)
```bash
python manage.py makemigrations
```

### Aplicar migraciones
```bash
python manage.py migrate
```

### Deshacer última migración
```bash
python manage.py migrate portfolio 0002  # Vuelve a migración anterior
```

### Acceder a Django Shell
```bash
python manage.py shell

# Ejemplos en shell:
from portfolio.models import Project, Profile
Profile.objects.get_active()
Project.objects.all()
Project.objects.filter(visible=True).count()
exit()
```

### Ver datos SQLite3 directo
```bash
sqlite3 db.sqlite3

# Comandos SQL:
SELECT * FROM portfolio_project;
SELECT COUNT(*) FROM portfolio_project WHERE visible=1;
.tables
.exit
```

---

## 👤 Gestión de Usuarios Admin

### Crear nuevo superuser
```bash
python manage.py createsuperuser
```

### Cambiar contraseña de usuario existente
```bash
python manage.py changepassword franchesemanuel
```

### Listar usuarios
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.all()
```

---

## 🔍 Verificación y Diagnóstico

### Verificar salud del sistema Django
```bash
python manage.py check
```

### Ver variables de configuración
```bash
python manage.py shell
>>> from django.conf import settings
>>> settings.DEBUG
>>> settings.ALLOWED_HOSTS
>>> settings.DATABASES
```

### Ver migraciones pendientes
```bash
python manage.py showmigrations | grep "\-"
```

### Ver estadísticas de base de datos
```bash
python manage.py shell
>>> from portfolio.models import *
>>> f"Perfiles: {Profile.objects.count()}"
>>> f"Proyectos: {Project.objects.count()}"
>>> f"Servicios: {Service.objects.count()}"
>>> f"Mensajes: {ContactMessage.objects.count()}"
```

---

## 📦 Gestión de Paquetes

### Ver paquetes instalados
```bash
pip list
```

### Instalar nuevo paquete
```bash
pip install nombre-paquete
```

### Actualizar paquete existente
```bash
pip install --upgrade nombre-paquete
```

### Actualizar requirements.txt
```bash
pip freeze > requirements.txt
```

---

## 🎨 Desarrollo Frontend

### Recompilar CSS si haces cambios
```bash
# No necesario - Django lo carga automáticamente
# Pero si usas Sass:
sass static/portfolio/scss/style.scss static/portfolio/css/style.css --watch
```

### Recolectar archivos estáticos (para producción)
```bash
python manage.py collectstatic --noinput
```

---

## 🚀 Preparación para Producción

### Crear archivo .env (variables secretas)
```bash
echo "DEBUG=False" > .env
echo "SECRET_KEY=tu-clave-super-secreta-aqui" >> .env
echo "ALLOWED_HOSTS=tudominio.com,www.tudominio.com" >> .env
```

### Generar SECRET_KEY segura
```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

### Hacer backup de base de datos
```bash
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)
```

### Restaurar desde backup
```bash
cp db.sqlite3.backup.20250129 db.sqlite3
```

---

## 🐛 Debugging

### Activar DEBUG mode (desarrollo solamente)
```bash
python manage.py runserver --debug
```

### Ver logs detallados de errores
```bash
# Los errores aparecen en la terminal del servidor
# Si está en background, ver con:
tail -f console.log
```

### Usar Django Debug Toolbar (requiere instalación)
```bash
pip install django-debug-toolbar
# Luego agregar a INSTALLED_APPS en settings.py
# Ver: https://django-debug-toolbar.readthedocs.io/
```

---

## 📧 Email (Configuración)

### Probar envío de email en shell
```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail(
...     'Asunto',
...     'Mensaje',
...     'from@example.com',
...     ['to@example.com'],
...     fail_silently=False,
... )
>>> # Si retorna 1 = éxito, 0 = fallo
```

---

## 🔄 Deployment Scripts

### Script para hacer backup automático (cron)
```bash
#!/bin/bash
# archivo: /home/portfolio/backup.sh

BACKUP_DIR="/home/portfolio/backups"
mkdir -p $BACKUP_DIR
cp /home/portfolio/portfolio/db.sqlite3 $BACKUP_DIR/db.sqlite3.$(date +%Y%m%d_%H%M%S)

# Eliminar backups de hace más de 30 días
find $BACKUP_DIR -name "*.sqlite3.*" -mtime +30 -delete
```

Agregar a cron:
```bash
crontab -e
# Agregar línea:
0 2 * * * /home/portfolio/backup.sh  # Ejecutar a las 2 AM diariamente
```

---

## 🔐 Security (Buenas Prácticas)

### Cambiar SECRET_KEY regularmente
```bash
# Generar nueva clave
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Actualizar en settings.py
# SECRET_KEY = 'nuevo-valor'

# Cambiar todas las sesiones activas
python manage.py clearsessions
```

### Deshabilitar DEBUG en producción
```python
# En settings.py:
DEBUG = False  # ¡CRÍTICO!

# Definir ALLOWED_HOSTS
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']

# Configurar HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🧹 Mantenimiento Rutinario

### Limpiar sesiones expiradas
```bash
python manage.py clearsessions
```

### Eliminar mensajes de contacto antiguos (>1 año)
```bash
python manage.py shell
>>> from portfolio.models import ContactMessage
>>> from datetime import datetime, timedelta
>>> old = ContactMessage.objects.filter(created_at__lt=datetime.now()-timedelta(days=365))
>>> count = old.count()
>>> old.delete()
>>> print(f"Eliminados {count} mensajes")
```

### Optimizar base de datos
```bash
sqlite3 db.sqlite3 "VACUUM;"
```

---

## 📊 Monitoreo

### Ver uso de memoria
```bash
# macOS
ps aux | grep python

# Linux
top
```

### Ver logs del servidor (en producción con gunicorn)
```bash
# Último 100 líneas
journalctl -u gunicorn -n 100

# Seguir en tiempo real
journalctl -u gunicorn -f

# Desde inicio del día
journalctl -u gunicorn --since today
```

---

## 🚀 Deploy Commands (Heroku)

```bash
# Login
heroku login

# Crear app
heroku create tu-app-name

# Push
git push heroku main

# Ver logs
heroku logs --tail

# Run comando
heroku run python manage.py migrate

# SSH
heroku run bash
```

---

## 🚀 Deploy Commands (DigitalOcean)

```bash
# SSH al servidor
ssh root@tu_servidor_ip

# Ver estatus de gunicorn
systemctl status gunicorn

# Reiniciar gunicorn
systemctl restart gunicorn

# Ver logs
journalctl -u gunicorn -f

# Actualizar código
cd /home/portfolio/portfolio
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
systemctl restart gunicorn
```

---

## 📝 Tips Útiles

### Crear archivo .gitignore
```bash
cat > .gitignore << 'EOF'
# Python
*.py[cod]
__pycache__/
*.so
.Python
venv/
env/
.venv

# Django
*.sqlite3
*.sqlite3-journal
/media
/staticfiles
.env
local_settings.py

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
EOF
```

### Guardar estado actual del proyecto
```bash
git add .
git commit -m "Portfolio CMS - Versión completa con documentación"
git push
```

### Ver cambios sin guardar
```bash
git status
git diff
```

---

## 🆘 Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| "Port already in use" | `lsof -i :8000` luego `kill -9 PID` |
| "No module named 'portfolio'" | `cd` a la carpeta correcta, activar .venv |
| "Database locked" | Cerrar otra conexión: `fuser -k db.sqlite3` |
| "Admin login falla" | `python manage.py changepassword franchesemanuel` |
| "Cambios no aparecen" | Recargar: `Ctrl+Shift+R` (hard refresh) |
| "Imágenes no cargan" | Verificar: `python manage.py check`, reiniciar servidor |
| "CSS no carga" | Ejecutar: `python manage.py collectstatic` |
| "Migration error" | Ver: `python manage.py showmigrations` |

---

## 📚 Documentación Oficial

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Templates](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

---

## 💾 Backup & Restore

### Backup completo del proyecto
```bash
tar -czf portfolio-backup-$(date +%Y%m%d).tar.gz \
  --exclude=".venv" \
  --exclude="__pycache__" \
  --exclude=".git" \
  /Users/francoemanuelsalcedo/Desktop/porfolio/
```

### Restaurar
```bash
tar -xzf portfolio-backup-20250129.tar.gz -C /path/to/restore
```

---

**¡Guardador este archivo como referencia rápida!** 🚀

Última actualización: Enero 2025
