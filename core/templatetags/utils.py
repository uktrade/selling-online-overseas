import urllib
from django import template


register = template.Library()


@register.simple_tag
def breadcrumblink(query, *params):
    """
    Format query string, according passed paramseters
    """
    par = urllib.parse.parse_qs(query)
    queryparams = ''
    for param in params:
        if param in par:
            for value in par[param]:
                queryparams += "{0}={1}&".format(param, value)

    return queryparams[:-1].replace(' ', '+')


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


@register.filter(name='countries')
def get_countries(market):
    """
    Get a comma-separated list of countries the Market's serves
    """

    country_list = list(set([str(country) for country in market.countries_served.all()]))
    country_list.sort(key=lambda country: country)
    return ", ".join(set(country_list))
