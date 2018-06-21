from django import forms
from . import models


class CreateRecipe(forms.ModelForm):
    class Meta:
        model = models.Recipe
        fields = ['title', 'description', 'thumbnail']
