from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from utils.models import Country, UnitMeasure, Currency
from ingredients.models import Ingredient


# Create your models here.


class RecipeType(models.Model):
    """
    Model to represent a recipe type
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class RecipeSkill(models.Model):
    """
    Model to represent the skill needed to cook this recipe
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    value = models.IntegerField(default=0)

    def __str__(self):
        return '%s' % self.name


class RecipeCost(models.Model):
    cost = models.IntegerField(default=0)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return '%f %s' % (self.cost,
                          self.currency.symbol)


class Recipe(models.Model):
    """
    Model to represent a recipe
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    thumbnail = models.ImageField(default='default/default_recipe.png', upload_to='images/recipes', blank=True)
    preparation_time = models.IntegerField(default=0)
    cooking_time = models.IntegerField(default=0)
    cooling_time = models.IntegerField(default=0)
    median_rate = models.FloatField(default=0)
    published = models.BooleanField(default=False)
    # Foreign Keys
    recipe_type = models.ForeignKey(RecipeType, on_delete=models.CASCADE)
    recipe_skill = models.ForeignKey(RecipeSkill, on_delete=models.CASCADE)
    recipe_origin = models.ForeignKey(Country, on_delete=models.CASCADE)
    recipe_cost = models.OneToOneField(RecipeCost, on_delete=models.CASCADE, null=True)
    # MetaData
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    published_at = models.DateTimeField(null=True)

    def __str__(self):
        return '%s - %s by %s' % (self.name,
                                  self.recipe_skill.name,
                                  self.author.username)

    def get_short_description(self):
        return '%s...' % self.description[:100]

    def get_median_rate(self):
        avg = self.rates.aggregate(Avg('rate')).get('rate__avg')
        return '0' if avg is None else str(avg).replace(',', '.')


class RecipeStep(models.Model):
    """
    Model to represent a recipe preparation step
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    order = models.IntegerField(default=0)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '%s in %s' % (self.name,
                             self.recipe.name)

    def get_short_description(self):
        return '%s...' % self.description[:50]


class RecipeIngredient(models.Model):
    """
    Model to represent a recipe ingredient (see ingredient model in generic app)
    """
    quantity = models.FloatField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit_measure = models.ForeignKey(UnitMeasure, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return '%s - Quantity : %d %s in %s' % (self.ingredient.name,
                                                self.quantity,
                                                self.unit_measure.symbol,
                                                self.recipe.name)


class RecipeImage(models.Model):
    """
    Model to represent some pictures added after the creation of the recipe
    """
    name = models.CharField(max_length=100)
    image = models.ImageField(default='default/default_recipe.png', upload_to='images/recipes', blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='images')
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s (%s) from %s' % (self.name,
                                    self.image.url,
                                    self.recipe.name)


class RecipeComment(models.Model):
    """
    Model to represent a comment written by a user for a recipe
    """
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return 'Comment %d from %s for recipe %s' % (self.pk,
                                                     self.user.username,
                                                     self.recipe.name)

    def get_children(self):
        return RecipeComment.objects.filter(parent=self)

    def is_root(self):
        return self.parent is None


class RecipeRate(models.Model):
    """
    Model to represent a rate done by a user to a recipe
    """
    rate = models.FloatField(default=-1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='rates')

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return 'Rate of %d by %s for recipe %s' % (self.rate,
                                                   self.user.username,
                                                   self.recipe.name)
