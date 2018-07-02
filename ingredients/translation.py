from modeltranslation.translator import register, TranslationOptions
from .models import IngredientType


@register(IngredientType)
class IngredientTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)
