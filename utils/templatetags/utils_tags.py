from django import template
from recipes.models import RecipeType, RecipeSkill

register = template.Library()


@register.inclusion_tag('utils/_browse_menu.html')
def advanced_search_menu():
    return {'types': RecipeType.objects.all(), 'skills': RecipeSkill.objects.all()}


@register.inclusion_tag('utils/_footer_menu_type.html')
def footer_category_menu():
    return {'types': RecipeType.objects.all()}


@register.inclusion_tag('utils/_footer_menu_skill.html')
def footer_skill_menu():
    return {'skills': RecipeSkill.objects.all()}
