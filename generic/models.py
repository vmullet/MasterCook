from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    css_class = models.CharField(max_length=50)


class UnitMeasure(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=10)

