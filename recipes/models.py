from django.db import models
from accounts.models import CookerProfile
from generic.models import Country, UnitMeasure
from ingredients.models import Ingredient


# Create your models here.


class RecipeType(models.Model):
    """
    Model to represent a recipe type
    """
    name = models.CharField(max_length=100)
    description = models.TextField

    def __str__(self):
        return self.name


class RecipeSkill(models.Model):
    """
    Model to represent the skill needed to cook this recipe
    """
    name = models.CharField(max_length=100)
    description = models.TextField
    value = models.IntegerField(default=0)

    def __str__(self):
        return '%d - %d'.format(self.name, self.value)


class Recipe(models.Model):
    """
    Model to represent a recipe
    """
    name = models.CharField(max_length=100)
    description = models.TextField
    thumbnail = models.ImageField(default='default.png', blank=True)
    recipe_type = models.ForeignKey(RecipeType, on_delete=models.CASCADE)
    recipe_skill = models.ForeignKey(RecipeSkill, on_delete=models.CASCADE)
    recipe_origin = models.ForeignKey(Country, on_delete=models.CASCADE)
    author = models.ForeignKey(CookerProfile, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return '%s - %s by %s'.format(self.name,
                                      self.recipe_skill.name,
                                      self.author.user.username)


class RecipeStep(models.Model):
    """
    Model to represent a recipe preparation step
    """
    name = models.CharField(max_length=100)
    description = models.TextField
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return '%s in %s'.format(self.name, self.recipe.name)


class RecipeIngredient(models.Model):
    """
    Model to represent a recipe ingredient (see ingredient model in generic app)
    """
    quantity = models.FloatField
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit_measure = models.ForeignKey(UnitMeasure, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - Quantity : %d %s in %s'.format(self.ingredient.name,
                                                    self.quantity,
                                                    self.unit_measure.symbol,
                                                    self.recipe.name)


class RecipeImage(models.Model):
    """
    Model to represent some pictures added after the creation of the recipe
    """
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default.png', blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return '%s (%s) from %s'.format(self.name, self.image.url, self.recipe.name)
