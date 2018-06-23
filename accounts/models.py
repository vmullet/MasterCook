from django.db import models
from django.contrib.auth.models import User
from generic.models import Country

# Create your models here.


class CookerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    avatar = models.ImageField(default='default_avatar.png', blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)



