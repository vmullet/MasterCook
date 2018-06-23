from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CookerAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'aria-describedby': 'sizing-addon1',
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'aria-describedby': 'sizing-addon1',
        }
    ))
