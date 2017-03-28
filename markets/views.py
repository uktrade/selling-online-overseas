import json
import ast
import csv

from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.forms import TypedChoiceField
from django.db.models import Max, Case, When, FloatField, ExpressionWrapper, Count, F
from django.http import Http404

from thumber.decorators import thumber_feedback

from .models import Market, PublishedMarket
from .forms import MarketListFilterForm
from core.forms import QueryChoiceMixin
from products.models import Category
from geography.models import Country


class MarketFilterMixin(object):
    """
    """

    @property
    def markets(self):
        if not self.request:
            authenticated = False
        else:
            authenticated = self.request.user.is_authenticated()

        if not authenticated:
            # Remove the not published Markets for un-authed users
            return PublishedMarket.objects
        else:
            return Market.objects


class HomepageView(MarketFilterMixin, TemplateView):
    """
    The landing page for the e-marketplace finding tool, offering advice on it's use
    """

    template_name = 'markets/homepage.html'

    def get_context_data(self, *args, **kwargs):
        """
        Include the count of markets in the context data for showing on the homepage
        """

        context = super().get_context_data(*args, **kwargs)
        context['market_count'] = self.markets.count()
        context['last_updated'] = self.markets.aggregate(Max('last_modified'))['last_modified__max']
        return context


class SearchView(MarketFilterMixin, TemplateView):
    """
    The first step in the tool, used to pre-filter the marketplaces
    """

    template_name = 'markets/search.html'

    def get_context_data(self, *args, **kwargs):
        """
        Include the starting results_count in the rendering as the total count of Markets
        """

        context = super().get_context_data(*args, **kwargs)
        context['results_count'] = self.markets.count()
        return context


@thumber_feedback
class MarketListView(MarketFilterMixin, ListView):
    """
    View for producing a list of Markets based on some user-selected filtering
    """

    satisfied_wording = "Did you find what you were looking for?"
    template_name = 'markets/list.html'
    context_object_name = 'markets_list'

    def get_context_data(self, *args, **kwargs):
        """
        Include the filtering form (pre-populated with the request's GET args) in the response
        """

        context = super().get_context_data(*args, **kwargs)
        context['form'] = MarketListFilterForm(self.request.GET)
        return context

    def _clean_params(self):
        """
        Clean up the GET params, discarding empty values, values = '*', and try to infer the correct type of each
        """

        get_params = {}

        for key, items in self.request.GET.lists():
            # For each submitted item, clean up the values
            cleaned_items = []
            for item in items:
                # We don't want '' or '*'
                if item != '*' and item != '':
                    try:
                        # Try and convert to true types, e.g. 'True' to True, and '1' to 1
                        cleaned_items.append(ast.literal_eval(item))
                    except (ValueError, SyntaxError):
                        # Failed to get a literal, just use the supplied string
                        cleaned_items.append(item)

            # Discard any attributes that had no valid values submitted
            if len(cleaned_items) > 0:
                get_params[key] = cleaned_items

        return get_params

    def get_queryset(self):
        """
        Filter the Markets based on GET parameters.  Parameters of '*' are ignored, as we need a way to pass certain
        GET params and have them not be restrictive of the resultset.  Valid attributes of the Market are converted
        into __in selectors

        eg. URL args of:
                ?name=Foo&operating_countries__name=uk&boolen_field=True&invalid_property=blah
            will be result in:
                Market.objects.filter(name__in=['Foo'], operating_countries__name=['uk'], boolen_field__in=[True])
        """

        # Get the cleaned get parameters
        get_params = self._clean_params()

        # Initialise a form with the cleaned GET data
        form = MarketListFilterForm(get_params)

        # Create a filter dictionary to store the requested filters
        _filter = {}

        for bound_field in form:
            if isinstance(bound_field.field, QueryChoiceMixin):
                attr = bound_field.field.attribute
            else:
                attr = bound_field.name

            value = bound_field.value()
            if value is not None:
                _filter["{}__in".format(attr)] = value

        for key, items in get_params.items():
            if key in form.fields:
                # This is a form field, already dealt with above
                continue

            attr = key.split('__')[0]
            try:
                # See if this is actually a property of the Market (or a property of another attached model)
                Market._meta.get_field(attr)

                # Turn the property into a filter selector, need to use __in since it's a list of values
                _filter["{}__in".format(key)] = items
            except:
                # Ignore GET params that aren't on the model
                pass

        markets = self._order_markets(_filter)

        return markets

    def _order_markets(self, orig_filter):
        # We will need to apply a different filter to the query than the original passed in, store it here
        new_filter = {}
        # Build annotations for each of the __in filters
        annotations = {}

        category_filter = orig_filter.pop('product_categories__name__in', [])
        matches, score = self._order_by_related_model_name('product_categories__name__in', category_filter)
        annotations['product_categories_matches'] = matches
        annotations['product_categories_score'] = score
        annotations['total_score'] = score

        country_filter = orig_filter.pop('operating_countries__name__in', [])
        matches, score = self._order_by_related_model_name('operating_countries__name__in', country_filter)
        annotations['operating_countries_matches'] = matches
        annotations['operating_countries_score'] = score
        annotations['total_score'] += score

        # Filter the markets based on the original search params (without the product/category terms)
        markets = self.markets.filter(**orig_filter)

        # Make the filter term to ensure we only have results where there is more than 1 match for each filter term
        new_filter = {'product_categories_matches__gt': 0, 'operating_countries_matches__gt': 0}

        # Apply all the annotations to the queryset
        return markets.annotate(**annotations).filter(**new_filter).order_by('-total_score')

    def _order_by_related_model_name(self, attribute, values):

        # Get the related model from the attribute
        related_model_name = attribute[:attribute.index('__')]
        related_model = getattr(Market, related_model_name).rel.model
        search_count = len(values)

        # Get rid of the trailing '__in'
        attr_name = attribute[:-4]

        # Get the name of the related model as a field in the query
        field_name = F('{0}__name'.format(related_model_name))

        if search_count > 0:
            # The user has filtered this related model, so calculate a score based on matching values, with a modifier
            # for unmatched values

            when_statements = []

            for value in values:
                # Construct When objects like When(related_model='value', then=blah)
                # 'blah' in this case is the name of the model, as this will be COUNT(DISTINCT) later
                when_kwargs = {attr_name: value, 'then': field_name}
                when_statements.append(When(**when_kwargs))

            # Get the number of matches for the related model
            matches = Count(Case(*when_statements, default=None, output_field=FloatField()), distinct=True)
            # Get the total number of the related model the market has
            total = ExpressionWrapper(Count(field_name, distinct=True), output_field=FloatField())
            # Calculate an irrelevance score, based the unmatched values
            irrelevance = ExpressionWrapper((1.0 * (total - matches) / total), output_field=FloatField())
            # Compute the overall score
            score = ExpressionWrapper(((matches - irrelevance) / search_count), output_field=FloatField())
        else:
            # The user did NOT filter this related model, so calculate based on all relations to the market counting
            # as a match, and divide by the total number of the related model in the database

            count = related_model.objects.count()
            matches = Count(field_name, distinct=True)
            score = ExpressionWrapper((1.0 * matches / count), output_field=FloatField())

        return matches, score


class MarketCountView(MarketListView):
    """
    A simple AJAX view that the filtering page calls to query the number of Markets will result from the currently
    selected filters
    """

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(
            {'count': self.object_list.count()},
            **response_kwargs
        )


class MarketStatsCountView(MarketListView):
    """
    A simple AJAX view for geckoboard integration to get the count of the live marketplaces
    """

    def render_to_response(self, context, **response_kwargs):
        data = {'item': [{'value': self.object_list.count(), 'text': 'Live marketplaces'}]}
        return JsonResponse(data, **response_kwargs)


class MarketStatsUpdateView(MarketListView):
    """
    A simple AJAX view for geckoboard integration to get the date of the most recent update to the Markets
    """

    def render_to_response(self, context, **response_kwargs):
        last_updated_max = self.markets.aggregate(Max('last_modified'))['last_modified__max']
        data = {'item': [{'text': last_updated_max.strftime('%d %b %Y'), 'type': 2}]}
        return JsonResponse(data, **response_kwargs)


class MarketAPIView(MarketListView):
    """
    API view for rendering just the markets list, that can be embedded into the page asynchronously
    """

    template_name = 'markets/includes/market_list.html'


@thumber_feedback
class MarketDetailView(MarketFilterMixin, TemplateView):
    """
    The simple view for the details page for individual Markets
    """

    satisfied_wording = "Was this page useful?"
    template_name = 'markets/detail.html'

    def get_context_data(self, *args, **kwargs):
        """
        """

        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs['slug']

        try:
            context['market'] = self.markets.get(slug=slug)
        except (Market.DoesNotExist, PublishedMarket.DoesNotExist):
            raise Http404('Market does not exist')

        return context
