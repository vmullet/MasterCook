from django.contrib import admin
from .models import Country, UnitMeasure, Currency
from modeltranslation.admin import TranslationAdmin

# Register your models here.


class CountryAdmin(TranslationAdmin):
    pass


class CurrencyAdmin(TranslationAdmin):
    pass


class UnitMeasureAdmin(TranslationAdmin):
    pass


admin.site.register(Country, CountryAdmin)
admin.site.register(UnitMeasure, UnitMeasureAdmin)
admin.site.register(Currency, CurrencyAdmin)
