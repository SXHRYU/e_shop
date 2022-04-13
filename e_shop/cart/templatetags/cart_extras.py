from typing import Iterable
from django import template


register = template.Library()

@register.filter(name='sum')
def sum_of_values(value: Iterable, arg):
    """
    QuerySet has iterable 'value', elements of which have 'arg', 
    for example, price of products in queryset. Function returns sum of 
    value.arg, or sum of products' prices as in example.
    """
    iterable = [getattr(item, arg) for item in value]
    return sum(iterable)
