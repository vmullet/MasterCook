from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import CookerProfile
from utils.models import Country
from datetime import datetime


class CookerAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Username"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Password"),
            'aria-describedby': 'sizing-addon1',
        },
    ), localize=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )


class CookerCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Username"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("First Name"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Last Name"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Email"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Password"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Re-enter your password"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )


class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("First Name"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Last Name"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Email"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )


class CookerChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Old Password"),
            'aria-describedby': 'sizing-addon1',
        },
    ), localize=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("New Password"),
            'aria-describedby': 'sizing-addon1',
        },
    ), localize=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Re-enter the new password"),
            'aria-describedby': 'sizing-addon1',
        },
    ), localize=True)


class CookerProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': _("Date of birth"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    bio = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': _("Biography"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'aria-describedby': 'sizing-addon1',
        }
    ), required=False)
    country = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True, queryset=Country.objects.all())

    def __init__(self, *args, **kwargs):
        super(CookerProfileForm, self).__init__(*args, **kwargs)
        self.initial["date_of_birth"] = datetime.strftime(self.instance.date_of_birth, "%Y-%m-%d")

    class Meta:
        model = CookerProfile
        fields = (
            'date_of_birth',
            'bio',
            'avatar',
            'country',
        )

