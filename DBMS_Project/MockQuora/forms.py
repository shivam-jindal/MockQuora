from django import forms
from django.contrib.auth.models import User
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class RegisterForm(forms.ModelForm):

    class Meta:
        model = UserProfile


