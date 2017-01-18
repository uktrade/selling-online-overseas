import os
from markets.models import Market, Logo
from geography.models import Country
from products.models import Category


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def create_market(**variable_data):

    market_data = get_market_data(**variable_data)

    if 'countries_served' not in variable_data:
        country = create_country('UK')
        countries_served = [country]
    else:
        countries_served = market_data.pop('countries_served')

    if 'product_categories' not in variable_data:
        category = create_category('Toys')
        product_categories = [category]
    else:
        product_categories = variable_data.pop('product_categories')

    if 'name' not in variable_data:
        variable_data['name'] = "Amazon"

    if 'logo' not in variable_data:
        logo = create_logo()
    else:
        logo = market_data.pop('logo')

    market = Market(**market_data)
    market.save()
    market.countries_served = countries_served
    market.product_categories = product_categories
    market.logo = logo
    market.save()
    return market


def get_market_data(**variable_data):
    """
    All basic fields that must be filled in to for a Market to be clean
    """

    if 'name' not in variable_data:
        variable_data['name'] = "Amazon"

    if 'description' not in variable_data:
        variable_data['description'] = "Lorem Ipsum"

    if 'web_address' not in variable_data:
        variable_data['web_address'] = "example.com"

    if 'registration_fees' not in variable_data:
        variable_data['registration_fees'] = 0

    if 'membership_fees' not in variable_data:
        variable_data['membership_fees'] = 0

    if 'fee_per_listing' not in variable_data:
        variable_data['fee_per_listing'] = True

    if 'deposit' not in variable_data:
        variable_data['deposit'] = 0

    return variable_data


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


def create_country(name):
    country, created = Country.objects.get_or_create(name=name)
    return country


def create_category(name):
    category, created = Category.objects.get_or_create(name=name)
    return category


def load_sample_png():
    f = open("{}/png/sample.png".format(CURRENT_DIRECTORY), "rb")
    return f
