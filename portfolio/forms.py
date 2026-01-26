from django import forms
from django.core.exceptions import ValidationError
import re
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
    name = forms.CharField(validators=[validate_name])
    email = forms.EmailField(validators=[validate_email])

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tuemail@example.com'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Tu mensaje'}),
        }