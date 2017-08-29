from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.generic import View

from markets.models import Market


class HomepageView(TemplateView):
    template_name = 'homepage.html'


class PingView(View):
    """
    Simple view for checking uptime, counts the number of Market models in the DB to ensure basic operation
    """

    def get(self, request, *args, **kwargs):
        return JsonResponse({'count': Market.objects.count()})
