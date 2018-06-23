from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class CookerAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.username.placeholder"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.password.placeholder"),
            'aria-describedby': 'sizing-addon1',
        },
    ), localize=True)


class CookerCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.username.placeholder"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.firstname.placeholder"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.lastname.placeholder"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    email = forms.EmailField(widget = forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.email.placeholder"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.password.placeholder"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.password2.placeholder"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
