from django.db import models
from utils.models import UnitMeasure

# Create your models here.


class IngredientType(models.Model):
    """
    Model to represent a basic ingredient type
    """
    name = models.CharField(max_length=50)
    description = models.TextField(default='')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Model to represent a basic ingredient
    """
    name = models.CharField(max_length=100)
    ingredient_type = models.ForeignKey(IngredientType, on_delete=models.CASCADE)
    description = models.TextField(default='')

    def __str__(self):
        return self.name
