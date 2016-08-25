from django.conf.urls import url
from . import views

app_name = 'navigator'

urlpatterns = [
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
]
