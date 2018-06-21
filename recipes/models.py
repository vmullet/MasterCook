from django.db import models

# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(default='default.png', blank=True)

    def __str__(self):
        return self.title

