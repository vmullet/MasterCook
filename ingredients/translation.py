from modeltranslation.translator import register, TranslationOptions
from .models import Ingredient, IngredientType


@register(IngredientType)
class IngredientTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


@register(Ingredient)
class IngredientTranslationOptions(TranslationOptions):
    fields = ('name',)
