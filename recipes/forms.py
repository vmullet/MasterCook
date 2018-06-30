from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Recipe, RecipeType, RecipeSkill, RecipeCost, RecipeImage, RecipeIngredient, RecipeStep, \
    RecipeComment, RecipeRate
from utils.models import Country, Currency, UnitMeasure
from ingredients.models import Ingredient


# MAIN FORMS

class RecipeCreateForm(forms.ModelForm):
    """
    Form to represent the creation of a recipe (basic informations)
    """
    name = forms.CharField(label=_('Recipe name'), widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Please enter the recipe name"),
        }
    ), localize=True)
    recipe_type = forms.ModelChoiceField(label=_('Type of the recipe'), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ), localize=True, queryset=RecipeType.objects.all())
    recipe_origin = forms.ModelChoiceField(label=_('Recipe origin country'), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ), localize=True, queryset=Country.objects.all())
    recipe_skill = forms.ModelChoiceField(label=_('Recipe skill needed'), widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ), localize=True, queryset=RecipeSkill.objects.all())
    description = forms.CharField(label=_('Description of the recipe'), widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': _("Please enter the description of the recipe"),
        }
    ), localize=True)
    thumbnail = forms.ImageField(label=_('Main picture of the recipe'), widget=forms.FileInput(
        attrs={
            'class': 'form-control',
        }
    ))
    preparation_time = forms.IntegerField(label=_('Preparation time (in minutes)'), widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
        }
    ), localize=True)
    cooking_time = forms.IntegerField(label=_('Cooking time (in minutes)'), widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
        }
    ), localize=True)
    cooling_time = forms.IntegerField(label=_('Cooling time (in minutes), if needed'), widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
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

    thumbnail = forms.ImageField(label=_('Main picture of the recipe'), widget=forms.FileInput(
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
    cost = forms.IntegerField(label=_('Cost of the recipe'), widget=forms.NumberInput(
        attrs={
            'class': 'form-control',
            'placeholder': _("Please enter the cost of the recipe"),
        }
    ), localize=True)
    currency = forms.ModelChoiceField(label=_('Currency (for the cost)'), widget=forms.Select(
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
            'placeholder': _("Title / Description of the picture"),
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
            'min': 0,
            'max': 5,
            'step': 0.5,
            'data-size': 'xs',
        }
    ))

    class Meta:
        model = RecipeRate
        fields = {
            'rate'
        }


class RecipeFilterForm(forms.Form):
    keyword = forms.CharField(label=_('Keyword'), widget=forms.TextInput(attrs={
        'class': 'form-control',
        'name': 'keyword',
    }), localize=True, required=False)
    filter = forms.ChoiceField(label=_('Filter By'), widget=forms.Select(attrs={
        'class': 'form-control',
        'name': 'filter'
    }),
                               choices=([
                                   ('name', _('Title')),
                                   ('recipe_rate', _('Average Rate')),
                                   ('recipe_skill__value', _('Skill needed')),
                                   ('preparation_time', _('Preparation Time')),
                                   ('published_at', _('Publication Date'))
                               ]), localize=True)
    order = forms.ChoiceField(label=_('Order By'), widget=forms.Select(attrs={
        'class': 'form-control',
        'name': 'order'
    }),
                              choices=([
                                  ('', _('Ascending')),
                                  ('-', _('Descending')),
                              ]), localize=True, required=False)

    def __init__(self, vkeyword, select_filter, select_order, *args, **kwargs):
        super(RecipeFilterForm, self).__init__(*args, **kwargs)
        self.fields['keyword'].initial = vkeyword
        self.fields['filter'].initial = select_filter
        self.fields['order'].initial = select_order
