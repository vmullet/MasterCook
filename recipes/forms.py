from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Recipe, RecipeType, RecipeSkill
from generic.models import Country


class CreateRecipe(forms.ModelForm):
    name = forms.CharField(label='toto', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe_name.placeholder"),
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    recipe_type = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True, queryset=RecipeType.objects.all())
    recipe_origin = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True, queryset=Country.objects.all())
    recipe_skill = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True, queryset=RecipeSkill.objects.all())
    description = forms.CharField(widget=forms.Textarea(
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
    ))
    preparation_time = forms.DurationField(widget=forms.TimeInput(
        attrs={
            'class': 'form-control',
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    cooking_time = forms.DurationField(widget=forms.TimeInput(
        attrs={
            'class': 'form-control',
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True)
    cooling_time = forms.DurationField(widget=forms.TimeInput(
        attrs={
            'class': 'form-control',
            'aria-describedby': 'sizing-addon1',
        }
    ), localize=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'name',
            'recipe_type',
            'recipe_origin',
            'recipe_skill',
            'description',
            'thumbnail',
            'preparation_time',
            'cooking_time',
            'cooling_time'
        ]
