from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Recipe, RecipeType, RecipeSkill, RecipeCost
from generic.models import Country, Currency


class RecipeCreateForm(forms.ModelForm):
    name = forms.CharField(label=_('form.recipe.name'), widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe_name.placeholder"),
        }
    ), localize=True)
    recipe_type = forms.ModelChoiceField(label=_('form.recipe.type'), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ), localize=True, queryset=RecipeType.objects.all())
    recipe_origin = forms.ModelChoiceField(label=_('form.recipe.country'), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ), localize=True, queryset=Country.objects.all())
    recipe_skill = forms.ModelChoiceField(label=_('form.recipe.skill'), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ), localize=True, queryset=RecipeSkill.objects.all())
    description = forms.CharField(label=_('form.recipe.description'), widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe.description.placeholder"),
        }
    ), localize=True)
    thumbnail = forms.ImageField(label=_('form.recipe.thumbnail'), widget=forms.FileInput(
        attrs={
            'class': 'form-control',
        }
    ))
    preparation_time = forms.DurationField(label=_('form.recipe.preparation_time'), widget=forms.TimeInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe.preparation_time.placeholder"),
        }
    ), localize=True)
    cooking_time = forms.DurationField(label=_('form.recipe.cooking_time'), widget=forms.TimeInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe.cooking_time.placeholder"),
        }
    ), localize=True)
    cooling_time = forms.DurationField(label=_('form.recipe.cooling_time'), widget=forms.TimeInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe.cooling_time.placeholder"),
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


class RecipeCostForm(forms.ModelForm):
    cost = forms.FloatField(label=_('form.recipe_cost.cost'), widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe_cost.cost.placeholder"),
        }
    ), localize=True)
    currency = forms.ModelChoiceField(label=_('form.recipe_cost.currency'), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ), localize=True, queryset=Currency.objects.all())

    class Meta:
        model = RecipeCost
        fields = (
            'cost',
            'currency'
        )
