from django.contrib import admin
from .models import IngredientType, Ingredient

# Register your models here.

admin.site.register(IngredientType)
admin.site.register(Ingredient)
