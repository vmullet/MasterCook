from modeltranslation.translator import register, TranslationOptions
from .models import Country, Currency, UnitMeasure


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Currency)
class CurrencyTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(UnitMeasure)
class UnitMeasureTranslationOptions(TranslationOptions):
    fields = ('name',)
