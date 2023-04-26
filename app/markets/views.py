from django.http import JsonResponse
from django.views.generic import TemplateView, View
from django.conf import settings

from django.utils.functional import cached_property

from django.db.models import Max
from django.http import Http404
from django.core.paginator import Paginator

from thumber.decorators import thumber_feedback

from geography.models import Country
from products.models import Category

from directory_cms_client.client import cms_api_client
from directory_cms_client.helpers import handle_cms_response_allow_404

from .models import PublishedMarket


@thumber_feedback
class HomepageView(TemplateView):
    """
    The landing page for the e-marketplace finding tool, offering advice on it's use
    """

    template_name = 'markets/homepage.html'
    comment_placeholder = 'We are sorry to hear that. Would you tell us why?'
    submit_wording = 'Send feedback'
    satisfied_wording = 'Was this service useful?'

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug='selling-online-overseas-homepage',
            language_code=settings.LANGUAGE_CODE,
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response_allow_404(response)

    def get_context_data(self, *args, **kwargs):
        """
        Include the count of markets in the context data for showing on the homepage
        """
        featured_case_studies = self.page.get('featured_case_studies', [])
        return super().get_context_data(
            *args, **kwargs,
            success_stories=featured_case_studies,
            page_type='LandingPage',
            countries=Country.objects.all().order_by('name'),
            categories=Category.objects.all().order_by('name'),
            market_count=PublishedMarket.objects.count(),
            last_updated=PublishedMarket.objects.aggregate(
                Max('last_modified'))['last_modified__max'],
            random_markets=PublishedMarket.objects.order_by('?')[:3]
        )


@thumber_feedback
class MarketListView(TemplateView):
    template_name = 'markets/list.html'
    # thumber attributes
    satisfied_wording = 'Did you find what you were looking for?'
    comment_placeholder = 'We are sorry to hear that. Would you tell us why?'
    submit_wording = 'Send feedback'

    def get(self, request):
        params = request.GET.dict()
        category_id = params.get('category_id')
        country_id = params.get('country_id')

        qs = PublishedMarket.objects.all()

        if category_id and category_id.isdigit():
            category_id = int(category_id)
            qs = qs.filter(product_categories__id=category_id)
        if country_id and country_id.isdigit():
            country_id = int(country_id)
            qs = qs.filter(operating_countries__id=country_id)

        paginator = Paginator(qs, 6)
        pagination_page = paginator.page(self.request.GET.get('page', 1))
        context = {
            'page_type': 'SearchResultsPage',
            'market_list': qs,
            'selected_country_id': country_id,
            'selected_category_id': category_id,
            'countries': Country.objects.all().order_by('name'),
            'categories': Category.objects.all().order_by('name'),
            'pagination_page': pagination_page,
        }
        context = self.get_context_data(**context)
        return self.render_to_response(context)


class MarketShortlistView(TemplateView):

    template_name = 'markets/shortlist.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        market_slugs = self.request.session.get('market_slugs', [])
        context['markets_list'] = PublishedMarket.objects.filter(slug__in=market_slugs)

        return context


class MarketShortlistAPI(View):

    def _standard_response(self):
        market_slugs = self.request.session.get('market_slugs', [])
        return JsonResponse({'success': True, 'market_slugs': market_slugs})

    def get(self, request):
        return self._standard_response()

    def post(self, request):
        slug = self.request.GET.get('slug', None)
        if slug is None:
            return JsonResponse({'success': False, 'error': 'no slug supplied'})

        market_slugs = self.request.session.get('market_slugs', [])

        if slug not in market_slugs:
            market_slugs.append(slug)

        self.request.session['market_slugs'] = market_slugs
        return self._standard_response()

    def delete(self, request):
        slug = self.request.GET.get('slug', None)
        if slug is None:
            self.request.session['market_slugs'] = []
            return self._standard_response()

        market_slugs = self.request.session.get('market_slugs', [])

        if slug in market_slugs:
            market_slugs.remove(slug)

        self.request.session['market_slugs'] = market_slugs
        return self._standard_response()


@thumber_feedback
class MarketDetailView(TemplateView):
    """
    The simple view for the details page for individual Markets
    """

    satisfied_wording = 'Was this page useful?'
    template_name = 'markets/detail.html'
    comment_placeholder = 'We are sorry to hear that. Would you tell us why?'
    submit_wording = 'Send feedback'

    def get_context_data(self, *args, **kwargs):
        """
        """

        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs['slug']

        try:
            context['page_type'] = 'MarketplacePage'
            context['market'] = PublishedMarket.objects.get(slug=slug)
        except PublishedMarket.DoesNotExist:
            raise Http404('Market does not exist')

        return context
