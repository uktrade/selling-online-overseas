from django.conf.urls import url
from . import views

app_name = 'markets'

urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='home'),
    url(r'^filter/$', views.SearchView.as_view(), name='search'),
    url(r'^search/$', views.MarketListView.as_view(), name='list'),
    url(r'^count\.json$', views.MarketCountView.as_view(), name='count'),
    url(r'^stats/count$', views.MarketStatsCountView.as_view(), name='stats_count'),
    url(r'^stats/update$', views.MarketStatsUpdateView.as_view(), name='stats_update'),
    url(r'^api/$', views.MarketAPIView.as_view(), name='api'),
    url(r'^details/(?P<slug>[\w-]+)/$', views.MarketDetailView.as_view(), name='detail'),
    url(r'^story/(?P<slug>[\w-]+)/$', views.CaseStoryView.as_view(), name='case_story'),
]
