from django.conf.urls import url
from . import views

app_name = 'products'

urlpatterns = [
    url(r'^api/$', views.query_categories, name='api'),
    url(r'^log/$', views.log_search_term, name='log'),
]
