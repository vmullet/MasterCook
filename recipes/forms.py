from django import forms
from django.utils.translation import ugettext_lazy as _
from . import models


class CreateRecipe(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe_name.placeholder"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    description = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe_description.placeholder"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    thumbnail = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'aria-describedby': 'sizing-addon1',
        }
    ), required=True)

    class Meta:
        model = models.Recipe
        fields = [
            'name',
            'description',
            'thumbnail',
        ]
