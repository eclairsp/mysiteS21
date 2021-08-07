from django import template

register = template.Library()

@register.filter(name='level')
def level(value):
    lvl_choices = {
        'HS': 'High School',
        'UG': 'Undergraduate',
        'PG': 'Postgraduate',
        'ND': 'No Degree',
    }

    return lvl_choices[value]