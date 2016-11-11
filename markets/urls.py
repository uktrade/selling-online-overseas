from django.conf.urls import url
from . import views

app_name = 'markets'

urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='home'),
    url(r'^filter/$', views.FilteringView.as_view(), name='filtering'),
    url(r'^search/$', views.MarketListView.as_view(), name='list'),
    url(r'^count\.json$', views.MarketCountView.as_view(), name='count'),
    url(r'^stats$', views.MarketStatsView.as_view(), name='stats'),
    url(r'^api/$', views.MarketAPIView.as_view(), name='api'),
    url(r'^details/(?P<slug>[\w-]+)/$', views.MarketDetailView.as_view(), name='detail'),
]
