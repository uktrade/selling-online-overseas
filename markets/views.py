import json
import ast

from django.http import JsonResponse
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.forms import TypedChoiceField

from .models import Market
from .forms import MarketFilterForm, FilteringForm
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

    form_class = FilteringForm
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
        context['form'] = MarketFilterForm(self.request.GET)
        return context

    def _get_field_filter(self, field):
        value = field.value()

        if value is None:
            return (None, None)

        if isinstance(field.field, QueryChoiceMixin):
            attr = field.field.attribute
        else:
            attr = field.name

        if type(value) is not list:
            value = [value]

        # Strip the '*'s from the submitted values
        cleaned_values = []
        for val in value:
            if val != '*' and val != '':
                try:
                    cleaned_value = ast.literal_eval(val)
                except:
                    cleaned_value = val

                cleaned_values.append(cleaned_value)

        if not cleaned_values:
            # No values left after stripping '*'s, so skip this one
            return (None, None)

        return (attr, cleaned_values,)

    def get_queryset(self):
        """
        Filter the Markets based on GET parameters.  Parameters of '*' are ignored, as we need a way to pass certain
        GET params and have them not be restrictive of the resultset.  Valid attributes of the Market are converted
        into __in selectors

        eg. URL args of:
                ?name=Foo&countries_served__name=uk&invalid_property=blah
            will be result in:
                Market.objects.filter(name__in=['Foo'], countries_served__name=['uk'])
        """
        _filter = {}

        # Initialise a form with the GET data
        form = MarketFilterForm(self.request.GET)

        for bound_field in form:
            attr, value = self._get_field_filter(bound_field)
            if attr is not None:
                _filter["{}__in".format(attr)] = value

        for key, items in self.request.GET.lists():
            if key in form.fields:
                # This is a form field, already dealt with above
                continue

            # Get all get params to make into filters, ignoring '*'
            stripped_items = [x for x in items if x != '*']
            if not stripped_items:
                continue

            attr = key.split('__')[0]
            try:
                # See if this is actually a property of the Market (or a property of another attached model)
                Market._meta.get_field(attr)

                # Turn the property into a filter selector, need to use __in since it's a list of values
                _filter["{}__in".format(key)] = stripped_items
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
