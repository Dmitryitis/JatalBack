from django import forms
from django.contrib.auth.models import User


class AuthForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)


class RegistrationForm(forms.ModelForm):
    rep_password = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'password','first_name','last_name')
