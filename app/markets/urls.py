from django.conf.urls import url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'markets'

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'), permanent=True)),
    url(r'^filter/$', RedirectView.as_view(url=reverse_lazy('home'), permanent=True)),
    url(r'^results/$', views.MarketListView.as_view(), name='list'),
    url(r'^search/$', RedirectView.as_view(url=reverse_lazy('markets:list'), permanent=True)),
    url(r'^count\.json$', views.MarketCountView.as_view(), name='count'),
    url(r'^stats/count$', views.MarketStatsCountView.as_view(), name='stats_count'),
    url(r'^stats/update$', views.MarketStatsUpdateView.as_view(), name='stats_update'),
    url(r'^details/(?P<slug>[\w-]+)/$', views.MarketDetailView.as_view(), name='detail'),
    url(r'^story/(?P<slug>[\w-]+)/$', views.CaseStoryView.as_view(), name='case_story'),
    url(r'^shortlist/$', views.MarketShortlistView.as_view(), name='shortlist'),
    url(r'^api/shortlist/$', csrf_exempt(views.MarketShortlistAPI.as_view()), name='api_shortlist'),
]
