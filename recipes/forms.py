from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Recipe, RecipeType, RecipeSkill, RecipeCost, RecipeImage, RecipeIngredient, RecipeStep, RecipeComment, RecipeRate
from generic.models import Country, Currency, UnitMeasure
from ingredients.models import Ingredient


# MAIN FORMS

class RecipeCreateForm(forms.ModelForm):
    """
    Form to represent the creation of a recipe (basic informations)
    """
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
    preparation_time = forms.IntegerField(label=_('form.recipe.preparation_time'), widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe.preparation_time.placeholder"),
        }
    ), localize=True)
    cooking_time = forms.IntegerField(label=_('form.recipe.cooking_time'), widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe.cooking_time.placeholder"),
        }
    ), localize=True)
    cooling_time = forms.IntegerField(label=_('form.recipe.cooling_time'), widget=forms.NumberInput(
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


class RecipeEditForm(RecipeCreateForm):
    """
    Form to represent the edition of a recipe (basic informations)
    """

    thumbnail = forms.ImageField(label=_('form.recipe.thumbnail'), widget=forms.FileInput(
        attrs={
            'class': 'form-control',
        }
    ), required=False)

    def __init__(self, *args, **kwargs):
        super(RecipeEditForm, self).__init__(*args, **kwargs)
        self.fields.pop('name')

    class Meta:
        model = Recipe
        fields = (
            'recipe_type',
            'recipe_origin',
            'recipe_skill',
            'description',
            'thumbnail',
            'preparation_time',
            'cooking_time',
            'cooling_time'
        )


# SECONDARY FORMS (forms appended to the main forms)

class RecipeCostForm(forms.ModelForm):
    cost = forms.IntegerField(label=_('form.recipe_cost.cost'), widget=forms.NumberInput(
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


class RecipeImageForm(forms.ModelForm):
    """
    Form to represent the addition of a new image for the recipe
    """
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("form.recipe_name.placeholder"),
        }
    ), localize=True)
    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
        }
    ))

    class Meta:
        model = RecipeImage
        fields = {
            'name',
            'image'
        }


class RecipeStepForm(forms.ModelForm):
    """
    Form to represent the addition / edition of a RecipeStep
    """
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter the name of the step',
        }
    ), localize=True)
    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter the description of the step',
        }
    ), localize=True)

    class Meta:
        model = RecipeStep
        fields = {
            'name',
            'description'
        }


class RecipeIngredientForm(forms.ModelForm):
    """
    Form to represent the addition / edition of a RecipeIngredient
    """
    ingredient = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ), localize=True, queryset=Ingredient.objects.all())
    quantity = forms.IntegerField(widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Please enter a quantity',
        }
    ), localize=True)
    unit_measure = forms.ModelChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ), localize=True, queryset=UnitMeasure.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = {
            'ingredient',
            'quantity',
            'unit_measure'
        }


class RecipeCommentForm(forms.ModelForm):
    """
    Form to represent the addition / edition of a RecipeComment
    """
    comment = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter your comment',
        }
    ), localize=True)

    class Meta:
        model = RecipeComment
        fields = {
            'comment'
        }


class RecipeRateForm(forms.ModelForm):
    """
    Form to represent the addition / edition of a RecipeComment
    """
    rate = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': '',
            'data-size': 'xs',
        }
    ))

    class Meta:
        model = RecipeRate
        fields = {
            'rate'
        }
