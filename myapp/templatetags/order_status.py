from django import template

register = template.Library()


@register.filter(name='status')
def status(value):
    if value:
        ORD_STATUS_CHOICES = {0: 'Cancelled', 1: 'Confirmed', 2: 'On Hold'}

        return ORD_STATUS_CHOICES[value]
    return "Not provided!"