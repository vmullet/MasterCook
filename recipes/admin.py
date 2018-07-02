from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import RecipeType, \
    RecipeSkill, \
    RecipeStep, \
    RecipeIngredient, \
    RecipeImage, \
    RecipeRate, \
    RecipeComment, \
    Recipe


# Register your models here.

class RecipeTypeAdmin(TranslationAdmin):
    pass


class RecipeSkillAdmin(TranslationAdmin):
    pass


admin.site.register(Recipe)
admin.site.register(RecipeType, RecipeTypeAdmin)
admin.site.register(RecipeSkill, RecipeSkillAdmin)
admin.site.register(RecipeStep)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeImage)
admin.site.register(RecipeRate)
admin.site.register(RecipeComment)
