from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    css_class = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class UnitMeasure(models.Model):
    name = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return self.name

