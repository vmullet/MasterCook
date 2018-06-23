from django.contrib import admin
from .models import Country, UnitMeasure, Currency

# Register your models here.

admin.site.register(Country)
admin.site.register(UnitMeasure)
admin.site.register(Currency)
