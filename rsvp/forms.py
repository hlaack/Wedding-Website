from django import forms
from .models import Person, Family

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.hashers import check_password

from phonenumber_field.formfields import PhoneNumberField

class PasswordEntryForm(forms.Form):
    
    password_entry = forms.CharField(help_text='Enter your supplied password.', max_length=30, required=True)

    def clean_password_entry(self):
        data = self.cleaned_data['password_entry']
        hashed_pw = settings.RSVP_PASSWORD_HASH

        if not check_password(data, hashed_pw):
            raise ValidationError(_('Invalid password'))

        return data
    
class RsvpQueryForm(forms.Form):

    entered_first_name = forms.CharField(help_text='Enter your first name.', max_length=30, required=True)

    entered_last_name = forms.CharField(help_text='Enter your last name.', max_length=30, required=True)

    entered_email = forms.EmailField(help_text='Enter your email address.', max_length=50, required=True)

    entered_phone_num = PhoneNumberField(region="US")

    def clean_entered_last_name(self):
        last_name = self.cleaned_data['entered_last_name']

        if not Family.objects.filter(family_name__iexact=last_name).exists():
            raise ValidationError("We couldn't find a family with that last name. Please check and try again.")
        
    # def clean_entered_first_name(self):
    #     first_name = self.cleaned_data['entered_first_name']

    #     if not Person.objects.filter(first_name__iexact=first_name).exists():
    #         raise ValidationError("We couldn't find a person listed with that first name. Please check and try again.")

class RsvpPersonSelectForm(forms.Form):
    people = forms.ModelMultipleChoiceField(
        queryset=Person.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'check'}),
        required=False,
    )

    def __init__(self, *args, family=None, **kwargs):
        super().__init__(*args, **kwargs)
        if family is not None:
            self.fields['people'].queryset = family.people.all()

            attending_people = family.people.filter(status='y')
            self.fields['people'].initial = attending_people
