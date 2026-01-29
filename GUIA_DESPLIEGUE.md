# 🚀 GUÍA DE DESPLIEGUE A PRODUCCIÓN

## Fase Actual: Desarrollo Local ✅
Tu portfolio CMS está completamente funcional en `localhost:8000`. Este documento te guía para llevarlo a producción.

---

## 📋 Checklist Pre-Producción

### Seguridad
- [ ] Cambiar SECRET_KEY en `portfolio_project/settings.py`
- [ ] Cambiar contraseña del superuser
- [ ] Cambiar DEBUG = False
- [ ] Configurar ALLOWED_HOSTS con tu dominio
- [ ] Configurar CSRF_TRUSTED_ORIGINS
- [ ] Generar SECRET_KEY segura (128+ caracteres)

### Base de Datos
- [ ] Migrar a PostgreSQL (recomendado)
- [ ] Crear backup de db.sqlite3
- [ ] Configurar credenciales de base de datos
- [ ] Ejecutar migraciones en servidor

### Archivos Estáticos
- [ ] Ejecutar `collectstatic` para recopilar CSS, JS, imágenes
- [ ] Configurar servidor web (Nginx) para servir estáticos
- [ ] Optimizar imágenes antes de subir

### Email
- [ ] Configurar SMTP para enviar emails desde formulario de contacto
- [ ] Probar envío de correos
- [ ] Configurar EMAIL_BACKEND

### HTTPS/SSL
- [ ] Obtener certificado SSL (Let's Encrypt gratuito)
- [ ] Configurar SECURE_SSL_REDIRECT = True
- [ ] Configurar SESSION_COOKIE_SECURE = True
- [ ] Configurar CSRF_COOKIE_SECURE = True

---

## 🔧 Configuración para Producción

### 1. Generar SECRET_KEY Segura

```python
# En Django shell:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copia el output y reemplaza en `portfolio_project/settings.py`:

```python
SECRET_KEY = 'tu-nueva-clave-super-secreta-aqui'
```

### 2. Actualizar settings.py para Producción

```python
# Seguridad
DEBUG = False
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']
CSRF_TRUSTED_ORIGINS = ['https://tudominio.com', 'https://www.tudominio.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Base de datos (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tu_db_name',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_contraseña_segura',
        'HOST': 'localhost',  # o tu servidor RDS
        'PORT': '5432',
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # o tu proveedor
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña-app'
DEFAULT_FROM_EMAIL = 'tu-email@gmail.com'

# Analytics (opcional)
GOOGLE_ANALYTICS_ID = 'G-XXXXXXXXXX'  # Tu ID de Google Analytics
```

### 3. Archivos Estáticos

```bash
# En el servidor
python manage.py collectstatic --noinput
```

Configura Nginx para servir estáticos:

```nginx
location /static/ {
    alias /ruta/al/proyecto/staticfiles/;
}

location /media/ {
    alias /ruta/al/proyecto/media/;
}
```

---

## 🌐 Opciones de Despliegue

### Opción 1: Heroku (Más Fácil - Gratuito/Bajo Costo)

**Ventajas:** Fácil, automático, SSL incluido
**Desventajas:** Más caro a escala, menos control

```bash
# 1. Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Crear app
heroku create tu-app-name

# 4. Agregar base de datos
heroku addons:create heroku-postgresql:hobby-dev

# 5. Configurar variables de entorno
heroku config:set SECRET_KEY='tu-clave-secreta'
heroku config:set DEBUG=False

# 6. Crear Procfile
echo "web: gunicorn portfolio_project.wsgi" > Procfile

# 7. Actualizar requirements.txt
pip freeze > requirements.txt
# Agregar: gunicorn, whitenoise, dj-database-url, psycopg2-binary

# 8. Desplegar
git add .
git commit -m "Preparar para producción"
git push heroku main

# 9. Ejecutar migraciones
heroku run python manage.py migrate

# 10. Crear superuser
heroku run python manage.py createsuperuser
```

**URLs de Heroku:**
- Site: `https://tu-app-name.herokuapp.com/`
- Admin: `https://tu-app-name.herokuapp.com/admin/`

---

### Opción 2: DigitalOcean (Muy Popular - Bajo Costo)

**Ventajas:** Control total, barato, bueno para volúmenes medianos
**Desventajas:** Más configuración manual

```bash
# 1. Crear Droplet (Ubuntu 22.04, 4GB RAM)
# 2. SSH en el servidor
ssh root@tu_ip

# 3. Actualizar sistema
apt update && apt upgrade -y

# 4. Instalar dependencias
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx

# 5. Crear usuario y carpeta
useradd -m -s /bin/bash portfolio
cd /home/portfolio

# 6. Clonar proyecto
git clone tu-repo-aqui
cd portfolio

# 7. Crear virtual env
python3 -m venv venv
source venv/bin/activate

# 8. Instalar dependencias
pip install -r requirements.txt
pip install gunicorn psycopg2-binary whitenoise

# 9. Configurar PostgreSQL
sudo -u postgres psql << EOF
CREATE DATABASE portfolio_db;
CREATE USER portfolio_user WITH PASSWORD 'tu-contraseña-segura';
ALTER ROLE portfolio_user SET client_encoding TO 'utf8';
ALTER ROLE portfolio_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE portfolio_user SET default_transaction_deferrable TO on;
ALTER ROLE portfolio_user SET default_transaction_deferrable TO on;
ALTER ROLE portfolio_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;
EOF

# 10. Configurar gunicorn (crear archivo /home/portfolio/gunicorn.service)
# Ver template abajo

# 11. Configurar Nginx (ver template abajo)

# 12. Habilitar y iniciar servicios
systemctl enable gunicorn
systemctl start gunicorn
systemctl restart nginx
```

**Archivo: /etc/systemd/system/gunicorn.service**
```ini
[Unit]
Description=gunicorn daemon for portfolio
After=network.target

[Service]
User=portfolio
Group=www-data
WorkingDirectory=/home/portfolio/portfolio
ExecStart=/home/portfolio/portfolio/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/home/portfolio/portfolio/gunicorn.sock \
    portfolio_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Archivo: /etc/nginx/sites-available/portfolio**
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # Redirect HTTP a HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com www.tu-dominio.com;
    
    # SSL certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    
    client_max_body_size 20M;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/portfolio/portfolio/staticfiles/;
    }
    
    location /media/ {
        alias /home/portfolio/portfolio/media/;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/home/portfolio/portfolio/gunicorn.sock;
    }
}
```

---

### Opción 3: PythonAnywhere (Muy Simple - Ideal para Beginners)

**Ventajas:** Súper fácil, no requiere CLI, web-based
**Desventajas:** Menos flexibilidad

1. Ir a https://www.pythonanywhere.com/
2. Crear cuenta
3. Subir código vía Git
4. Crear app web Django
5. Configurar base de datos MySQL
6. Actualizar settings.py
7. Acceder a tu app en `tu-usuario.pythonanywhere.com`

---

## 🔒 Checklist de Seguridad Final

```
Pre-Producción:

[ ] SECRET_KEY cambiada a valor seguro (128+ chars)
[ ] DEBUG = False
[ ] ALLOWED_HOSTS actualizado
[ ] Contraseña de superuser cambiada
[ ] Email configurado correctamente
[ ] SSL/HTTPS habilitado
[ ] SECURE_SSL_REDIRECT = True
[ ] SESSION_COOKIE_SECURE = True
[ ] CSRF_COOKIE_SECURE = True
[ ] Base de datos respaldada
[ ] Archivos estáticos optimizados
[ ] Imágenes comprimidas
[ ] Requirements.txt actualizado
[ ] No hay secretos en git
[ ] .env file configurado (si usas)
[ ] Logs configurados
[ ] Monitoreo/alertas configurados
[ ] Dominio apunta a servidor
[ ] Certificado SSL válido
[ ] Backups automáticos configurados
```

---

## 📊 Monitoreo en Producción

### Logs
```bash
# Ver logs de gunicorn
journalctl -u gunicorn -f

# Ver logs de Nginx
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### Uptime Monitoring
- Usar UptimeRobot (https://uptimerobot.com/) - Gratuito
- Recibe alertas si tu sitio se cae

### Performance Monitoring
- New Relic (Gratis hasta cierto nivel)
- Sentry para error tracking
- Google Analytics para user analytics

### Backups
```bash
# Backup diario automático
0 2 * * * /home/portfolio/backup.sh

# Script backup.sh:
#!/bin/bash
BACKUP_DIR="/backups/portfolio"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump portfolio_db > $BACKUP_DIR/backup_$DATE.sql
gzip $BACKUP_DIR/backup_$DATE.sql
# Limpiar backups más viejos de 30 días
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
```

---

## 🎯 Próximos Pasos Después del Despliegue

1. **Dominio Personalizado**
   - Comprar dominio (Namecheap, GoDaddy)
   - Apuntar DNS a tu servidor
   - Esperar propagación (24-48 horas)

2. **Email Personalizado**
   - Configurar email en tu dominio
   - Si usas Gmail: Configurar SMTP
   - Si usas tu servidor: Instalar Postfix

3. **SEO**
   - Google Search Console
   - Bing Webmaster Tools
   - Sitemap.xml
   - robots.txt

4. **Análisis**
   - Google Analytics
   - Google Tag Manager
   - Heatmaps (Hotjar)

5. **Mejoras Continuas**
   - Monitoreo de performance
   - User feedback
   - A/B testing
   - Optimización de conversiones

---

## 🆘 Troubleshooting Común

### "502 Bad Gateway"
- Verificar que gunicorn está corriendo
- Verificar logs de gunicorn
- Verificar permisos de socket

### "STATIC FILES NO CARGAN"
- Ejecutar `collectstatic`
- Verificar permisos de carpeta
- Verificar configuración de Nginx

### "DATABASE CONNECTION ERROR"
- Verificar credenciales
- Verificar que PostgreSQL está corriendo
- Ejecutar migraciones

### "EMAILS NO SE ENVÍAN"
- Verificar credenciales SMTP
- Verificar puerto (587 para TLS)
- Verificar firewall/puertos

---

## 📞 Recursos Útiles

- [Django Deployment Guide](https://docs.djangoproject.com/en/6.0/howto/deployment/)
- [Heroku Docs](https://devcenter.heroku.com/)
- [DigitalOcean Community](https://www.digitalocean.com/community)
- [Let's Encrypt](https://letsencrypt.org/) - SSL Gratis
- [UptimeRobot](https://uptimerobot.com/) - Monitoreo Gratis

---

## 💰 Estimado de Costos Mensuales

| Servicio | Gratuito | Pago | Recomendado |
|----------|----------|------|-------------|
| **Hosting** | Heroku (limitado) | Heroku: $7-50/mes | DigitalOcean: $5-10/mes |
| **Base de Datos** | Incluido | PostgreSQL RDS: $15-50 | PostgreSQL en servidor |
| **Dominio** | — | $10-15/año | Namecheap: $10/año |
| **Email SMTP** | Gmail gratis (limitado) | SendGrid: $20+/mes | Gmail SMTP: Gratis |
| **SSL** | Let's Encrypt | Incluido en servicios | Let's Encrypt (gratis) |
| **Monitoreo** | Uptime Robot | New Relic: $29+/mes | Uptime Robot (gratis) |
| **TOTAL MÍNIMO** | $0 | $45/mes | $20/mes |

---

## ✅ Conclusión

Una vez completados estos pasos:

1. ✅ Tu portfolio estará en producción
2. ✅ Será accesible globalmente con tu dominio
3. ✅ Tendrá HTTPS seguro
4. ✅ Podrás seguir editando desde admin
5. ✅ Los usuarios verán cambios al instante

**Tu portfolio CMS está listo para el mundo! 🚀**

---

**Última actualización:** Enero 2025
**Versión:** 1.0
**Estado:** Listo para Producción
