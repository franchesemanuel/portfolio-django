from django import forms
from django.core.exceptions import ValidationError
import re
import bleach
from .models import ContactMessage

def validate_name(value):
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
        raise ValidationError('El nombre solo puede contener letras y espacios.')

def validate_email(value):
    # Regex más estricta para emails
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError('Ingresa un email válido en formato usuario@dominio.com')

class ContactForm(forms.ModelForm):
    name = forms.CharField(min_length=2, max_length=100, validators=[validate_name])
    email = forms.EmailField(max_length=254, validators=[validate_email])

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre completo',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tuemail@example.com',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Asunto de tu mensaje',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Cuéntame sobre tu proyecto o consulta...',
                'required': True
            }),
        }

    def clean_name(self):
        value = self.cleaned_data['name']
        cleaned = bleach.clean(value, tags=[], attributes={}, strip=True).strip()
        if len(cleaned) < 2:
            raise ValidationError('El nombre es demasiado corto.')
        return cleaned

    def clean_email(self):
        value = self.cleaned_data['email']
        cleaned = bleach.clean(value, tags=[], attributes={}, strip=True).strip().lower()
        return cleaned

    def clean_subject(self):
        value = self.cleaned_data.get('subject', '')
        cleaned = bleach.clean(value, tags=[], attributes={}, strip=True).strip()
        if not cleaned:
            raise ValidationError('El asunto es obligatorio.')
        if len(cleaned) < 4:
            raise ValidationError('El asunto es demasiado corto.')
        if len(cleaned) > 120:
            raise ValidationError('El asunto es demasiado largo (máx 120 caracteres).')
        return cleaned

    def clean_message(self):
        value = self.cleaned_data.get('message', '')
        cleaned = bleach.clean(value, tags=[], attributes={}, strip=True).strip()
        if len(cleaned) < 10:
            raise ValidationError('El mensaje es demasiado corto.')
        if len(cleaned) > 2000:
            raise ValidationError('El mensaje es demasiado largo (máx 2000 caracteres).')
        return cleaned
