# -*- coding: utf-8 -*-
import urllib

from django import template
from django.utils.safestring import mark_safe
from django.utils.numberformat import format

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
    Get a comma-separated list of values from a ManyToMany field
    """

    field = getattr(obj, attr)
    all_method = getattr(field, 'all', None)
    if all_method is None:
        return None

    value_list = list(set([str(item) for item in all_method()]))
    value_list.sort(key=lambda item: item)
    return ", ".join(set(value_list))


@register.filter(name='field_dd')
def render_field_options(obj, attr):
    """
    Render the dd elements for a related_model field with ticks/crosses for
    each item indicating if it's selected or not
    """

    field = getattr(obj, attr)
    resp = ""
    possible_vals = field.model.objects.all()
    actual_vals = field.all()
    for val in possible_vals:
        icon = tick_cross_format_field(val in actual_vals)
        resp += "<dd>{0} {1}</dd>".format(icon, val)

    return mark_safe(resp)


@register.filter(name='formatvalue')
def format_value(value, style):
    if style == 'required':
        resp = required_or_not_format_field(value)
    elif style == 'tick':
        resp = tick_cross_format_field(value)
    elif style == 'requiredtick':
        resp = required_tick_format_field(value)
    elif style == 'fee':
        resp = fee_format_field(value)
    else:
        resp = value

    return mark_safe(resp)


def fee_format_field(value):
    if value > 0:
        return "£{0}".format(format(value, '.', decimal_pos=2, grouping=3, thousand_sep=',', force_grouping=True))
    else:
        return required_or_not_format_field(False)


def required_tick_format_field(value):
    return "{0} {1}".format(tick_cross_format_field(value), required_or_not_format_field(value))


def required_or_not_format_field(value):
    if value:
        return "Required"
    else:
        return "Not required"


def tick_cross_format_field(value):
    if value:
        return icon_format_field('ok', 'ok')
    else:
        return icon_format_field('cross', 'cross')


def icon_format_field(icon, text='ok'):
    return '<i class="icon icon-details icon-' + icon + '"><span class="visuallyhidden">' + text + '</span></i>'
