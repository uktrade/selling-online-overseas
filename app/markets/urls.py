from django.conf.urls import url
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'markets'

urlpatterns = [
    url(r'^story/(?P<slug>[\w-]+)/$', RedirectView.as_view(url=reverse_lazy('home')), name='case_story_redirect'),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('home'), permanent=True)),
    url(r'^filter/$', RedirectView.as_view(url=reverse_lazy('home'), permanent=True)),
    url(r'^results/$', views.MarketListView.as_view(), name='list'),
    url(r'^search/$', RedirectView.as_view(url=reverse_lazy('markets:list'), permanent=True)),
    url(r'^details/(?P<slug>[\w-]+)/$', views.MarketDetailView.as_view(), name='detail'),
    url(r'^shortlist/$', views.MarketShortlistView.as_view(), name='shortlist'),
    url(r'^api/shortlist/$', csrf_exempt(views.MarketShortlistAPI.as_view()), name='api_shortlist'),
]
