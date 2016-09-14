import json
import ast

from django.http import JsonResponse
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.forms import TypedChoiceField

from .models import Market
from .forms import MarketListFilterForm, InitialFilteringForm
from core.forms import QueryChoiceMixin


class HomepageView(TemplateView):
    """
    The landing page for the e-marketplace finding tool, offering advice on it's use
    """

    template_name = 'markets/homepage.html'


class FilteringView(FormView):
    """
    The first step in the tool, used to pre-filter the marketplaces
    """

    form_class = InitialFilteringForm
    template_name = 'markets/filtering.html'

    def get_context_data(self, *args, **kwargs):
        """
        Include the starting results_count in the rendering as the total count of Markets
        """

        context = super().get_context_data(*args, **kwargs)
        context['results_count'] = Market.objects.count()
        return context


class MarketListView(ListView):
    """
    View for producing a list of Markets based on some user-selected filtering
    """

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
                ?name=Foo&countries_served__name=uk&boolen_field=True&invalid_property=blah
            will be result in:
                Market.objects.filter(name__in=['Foo'], countries_served__name=['uk'], boolen_field__in=[True])
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

        return Market.objects.filter(**_filter).distinct()


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


class MarketDetailView(DetailView):
    """
    The simple view for the details page for individual Markets
    """

    model = Market
    template_name = 'markets/detail.html'
    slug_field = 'slug'
