# -*- coding: utf-8 -*-
import urllib

from django import template
from django.utils.safestring import mark_safe
from django.utils.numberformat import format

register = template.Library()


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
    value_list.sort()
    return ", ".join(value_list)


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
    else:
        resp = value

    return mark_safe(resp)


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
