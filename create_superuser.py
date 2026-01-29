import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'franchesemanuel'
password = 'Savita1991'
email = 'franchesemanuel@example.com'

if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    print(f"El usuario '{username}' ya existe.")
    # Actualizar la contraseña por si acaso
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"Contraseña actualizada para '{username}'.")
else:
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"Superusuario '{username}' creado exitosamente.")

print(f"\nCredenciales:")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"URL Admin: http://127.0.0.1:8000/secure-admin/")
