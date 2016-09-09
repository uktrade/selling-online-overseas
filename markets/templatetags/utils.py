# -*- coding: utf-8 -*-
import urllib
from django import template


register = template.Library()


@register.filter(name='regions')
def get_regions(market):
    """
    Get a comma-separated list of regions the Market's serves
    """

    region_list = []
    for country in market.countries_served.all():
        if str(country.region) not in region_list:
            region_list.append(str(country.region))

    region_list.sort(key=lambda region: region)
    return ", ".join(region_list)


@register.filter(name='csl')
def comma_separated_list(obj, attr):
    """
    Get a command-separated list of values from a ManyToMany field
    """

    field = getattr(obj, attr)
    all_method = getattr(field, 'all', None)
    if all_method is None:
        return None

    value_list = list(set([str(item) for item in all_method()]))
    value_list.sort(key=lambda item: item)
    return ", ".join(set(value_list))


@register.filter(name='formatvalue')
def format_value(value, style):
    if style == 'required':
        return required_or_not_format_field(value)
    elif style == 'yesno':
        return yes_or_no_format_field(value)
    elif style == 'tick':
        return tick_cross_format_field(value)
    else:
        return value


def yes_or_no_format_field(value):
    if value:
        return "✔ Yes"
    else:
        return "✗ No"


def required_or_not_format_field(value):
    if value:
        return "✔ Required"
    else:
        return "✗ Not required"


def tick_cross_format_field(value):
    if value:
        return "✔"
    else:
        return "✗"
