from django import forms
from .models import RSVP_Protector

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.hashers import check_password

class PasswordEntryForm(forms.Form):
    
    password_entry = forms.CharField(help_text='Enter your supplied password.', max_length=30, required=True)

    def clean_password_entry(self):
        data = self.cleaned_data['password_entry']
        hashed_pw = settings.RSVP_PASSWORD_HASH

        if not check_password(data, hashed_pw):
            raise ValidationError(_('Invalid password'))

        return data
