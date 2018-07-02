from modeltranslation.translator import register, TranslationOptions
from .models import RecipeType, RecipeSkill


@register(RecipeType)
class RecipeTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


@register(RecipeSkill)
class RecipeSkillTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


