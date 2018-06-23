from django.db import models
from accounts.models import CookerProfile
from generic.models import Country

# Create your models here.


class RecipeType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class RecipeSkill(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    value = models.IntegerField(default=0)


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    recipe_type = models.ForeignKey(RecipeType, on_delete=models.CASCADE)
    description = models.TextField()
    recipe_skill = models.ForeignKey(RecipeSkill, on_delete=models.CASCADE)
    thumbnail = models.ImageField(default='default.png', blank=True)
    origin_country = models.ForeignKey(Country, on_delete=models.CASCADE)
    author = models.ForeignKey(CookerProfile, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title


class RecipeSteps(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

