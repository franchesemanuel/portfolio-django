from django.contrib.admin import AdminSite
# from django_otp.admin import OTPAdminSite


class SecureAdminSite(AdminSite):  # Cambio temporal: sin OTP
    """
    Admin Site protegido con OTP (2FA).
    Requiere configurar un dispositivo OTP para el usuario administrador.
    
    NOTA: OTP desactivado temporalmente para acceso inicial.
    """
    site_header = "Portfolio CMS Seguro"
    site_title = "Admin Seguro"
    index_title = "Panel de Administración"


admin_site = SecureAdminSite(name="secure_admin")
