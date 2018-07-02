from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import IngredientType, Ingredient

# Register your models here.


class IngredientTypeAdmin(TranslationAdmin):
    pass


class IngredientAdmin(TranslationAdmin):
    pass


admin.site.register(IngredientType, IngredientTypeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
