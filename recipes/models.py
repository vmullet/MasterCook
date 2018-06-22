from django.db import models
from accounts.models import CookerProfile

# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(default='default.png', blank=True)
    author = models.ForeignKey(CookerProfile, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

