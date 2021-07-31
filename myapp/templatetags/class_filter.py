from django import template

register = template.Library()

@register.filter(name='nav')
def class_filter_nav():
    return