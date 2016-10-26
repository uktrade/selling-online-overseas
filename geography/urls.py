from django.conf.urls import url
from . import views

app_name = 'geography'

urlpatterns = [
    url(r'^api/$', views.query_countries, name='api'),
]
