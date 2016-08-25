from django import template

register = template.Library()


@register.filter
def field_type(field):
    return field.field.widget.__class__.__name__
