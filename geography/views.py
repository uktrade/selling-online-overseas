from django.http import JsonResponse
from .models import Country


def query_countries(request):
    """
    A simple AJAX view that returns suggested countries for the countries search box
    """

    query = request.GET.get('q', None)

    if query is None:
        return {}

    countries = Country.objects.filter(name__istartswith=query).order_by('-name')
    country_names = [country.name for country in countries]

    return JsonResponse({"countries": country_names})
