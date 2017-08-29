from django.db.models import Q
from django.http import JsonResponse

from .models import Country


def query_countries(request):
    """
    A simple AJAX view that returns suggested countries for the countries search box
    """

    query = request.GET.get('q', None)

    if query is None or query == '':
        countries = []
    else:
        countries_set = Country.objects.filter(Q(name__istartswith=query) | Q(alternate_name__istartswith=query))
        countries = countries_set.order_by('-name')

    country_names = [country.name for country in countries]

    return JsonResponse({"countries": country_names})
