import os
from markets.models import Market, Logo, Country, Region


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def create_market(**variable_data):
    if 'region' in variable_data:
        region = variable_data.pop('region')
        if type(region) == str:
            region = create_region(region)
    else:
        region = create_region('Europe')

    if 'countries_served' not in variable_data:
        country = create_country('UK', region)
        countries_served = [country]
    else:
        countries_served = variable_data.pop('countries_served')

    if 'name' not in variable_data:
        variable_data['name'] = "Amazon"

    market = Market(**variable_data)
    market.save()
    market.countries_served = countries_served
    market.save()
    return market


def create_logo(**variable_data):
    if 'name' not in variable_data:
        variable_data['name'] = 'logo'
    if '_encoded_data' not in variable_data:
        variable_data['_encoded_data'] = (
            'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HA'
            'wCAAAAC0lEQVR4nGP6LwkAAiABG+faPgsAAAAASUVORK5CYII=')
    logo = Logo(**variable_data)
    logo.save()
    return logo


def create_country(name, region=None):
    if region is None:
        country = Country.objects.get(name=name)
    else:
        if type(region) == str:
            region = create_region(region)
        country, created = Country.objects.get_or_create(name=name, region=region)
    return country


def create_region(name):
    region, created = Region.objects.get_or_create(name=name)
    return region


def load_sample_png():
    f = open("{}/png/sample.png".format(CURRENT_DIRECTORY), "rb")
    return f
