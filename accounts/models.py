from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)


class CookerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)



