from django import forms
from django.core.validators import ValidationError
from django.contrib.auth.base_user import BaseUserManager

from datetime import datetime

from design.models.user import User, DesignerUser, BusinessUser
from design.helper import normalize_email

import email_normalize

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        fields = ('email','first_name', 'last_name')
        model = User

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        return normalize_email(email).normalized_address


    def save(self, commit=True):
        raise Warning('This method can not be used, use the create_user method in the user manager')
        return


class DesignerRegistrationForm(forms.ModelForm):
    class Meta:
        model = DesignerUser
        fields = ['years_experience']

class BusinessRegistrationForm(forms.ModelForm):
    class Meta:
        model = BusinessUser
        fields = ['business_name']






