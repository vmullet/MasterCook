from django.contrib import admin
from .models import RecipeType, \
    RecipeSkill, \
    RecipeStep, \
    RecipeIngredient, \
    RecipeImage, \
    RecipeRate, \
    RecipeComment, \
    Recipe

# Register your models here.

admin.site.register(Recipe)

admin.site.register(RecipeType)
admin.site.register(RecipeSkill)
admin.site.register(RecipeStep)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeImage)
admin.site.register(RecipeRate)
admin.site.register(RecipeComment)
