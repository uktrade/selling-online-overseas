from collections import OrderedDict

from whoosh.lang.porter import stem
from django.http import JsonResponse
from django.utils.text import Truncator

from .search import perform_category_query


def query_categories(request):
    """
    A simple AJAX view that returns suggested product categories based on supplied product terms
    """

    query_words = request.GET.get('q', None)

    if query_words is None:
        return {}

    results, suggestion = perform_category_query(stem(query_words))

    if len(query_words) > 3 and len(results) == 0 and suggestion is not None:
        query_words = suggestion
        results, suggestion = perform_category_query(query_words)

    ordered_categories = OrderedDict(sorted(results.items(), key=lambda x: len(x[1]), reverse=True))

    categories = []

    for category, sub_categories in ordered_categories.items():
        if category == 'Mature':
            categories.append([category, ""])
        else:
            categories.append([category, Truncator(", ".join(sub_categories)).words(8)])

    resp = {
        "query": query_words,
        "categories": categories,
        "suggestion": suggestion
    }

    return JsonResponse(resp)
