from django.db import models
from generic.models import UnitMeasure

# Create your models here.


class IngredientType(models.Model):
    """
    Model to represent a basic ingredient type
    """
    name = models.CharField(max_length=50)
    description = models.TextField()
    thumbnail = models.ImageField(default='default/default_ingredient_type.png', blank=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Model to represent a basic ingredient
    """
    name = models.CharField(max_length=100)
    ingredient_type = models.ForeignKey(IngredientType, on_delete=models.CASCADE)
    description = models.TextField
    thumbnail = models.ImageField(default='default/default_ingredient.png', blank=True)

    def __str__(self):
        return self.name
