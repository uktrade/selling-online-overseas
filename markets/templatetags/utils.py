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
