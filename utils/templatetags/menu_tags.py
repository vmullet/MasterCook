from django import template
from recipes.models import RecipeType, RecipeSkill

register = template.Library()


@register.inclusion_tag('utils/_browse_menu.html')
def advanced_search_menu():
    return {'types': RecipeType.objects.all(), 'skills': RecipeSkill.objects.all()}
