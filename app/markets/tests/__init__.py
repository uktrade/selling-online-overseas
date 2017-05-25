import os
from markets.models import Market, Logo
from geography.models import Country
from products.models import Category
from django.core.files.uploadedfile import SimpleUploadedFile


CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def create_market(**variable_data):

    market_data = get_market_data(**variable_data)

    if 'operating_countries' not in variable_data:
        country = create_country('UK')
        operating_countries = [country]
    else:
        operating_countries = market_data.pop('operating_countries')

    if 'product_categories' not in variable_data:
        category = create_category('Toys')
        product_categories = [category]
    else:
        product_categories = market_data.pop('product_categories')

    if 'name' not in variable_data:
        variable_data['name'] = "Amazon"

    if 'logo' not in variable_data:
        logo = create_logo()
    else:
        logo = market_data.pop('logo')

    market = Market(**market_data)
    market.save()
    market.operating_countries = operating_countries
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

    if 'e_marketplace_description' not in variable_data:
        variable_data['e_marketplace_description'] = "Lorem Ipsum"

    if 'web_address' not in variable_data:
        variable_data['web_address'] = "example.com"

    if 'one_off_registration_fee' not in variable_data:
        variable_data['one_off_registration_fee'] = 0

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
    if 'image' not in variable_data:
        folder = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(folder, 'png', 'sample.png')
        variable_data['image'] = SimpleUploadedFile(name='test.jpg',
                                                    content=open(image_path, 'rb').read(),
                                                    content_type='image/jpeg')

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
