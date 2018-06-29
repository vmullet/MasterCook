from django import template

register = template.Library()


@register.inclusion_tag('base_layout.html')
def main_menu(poll):
    pass
