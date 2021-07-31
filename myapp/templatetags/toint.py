from django import template

register = template.Library()

@register.filter(name='toint')
def to_int(value):
    return int(value)
