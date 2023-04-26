from django.conf.urls import url
from django.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView, RedirectView
from core.views import PingView
from markets.views import HomepageView
from activitystream.views import ActivityStreamViewSet
from django.urls import reverse_lazy

urlpatterns_unprefixed = [
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    url(r'^ping\.json$', PingView.as_view(), name='ping'),
    url(r'^grappelli/', include('grappelli.urls')),
    url('^auth/', include('authbroker_client.urls', namespace='authbroker')),
    url(r'^admin/login/$', RedirectView.as_view(url=reverse_lazy('authbroker:login'), query_string=True)),
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomepageView.as_view(), name='home'),
    url(r'^markets/', include('markets.urls'), name='markets'),
    url(r'^products/', include('products.urls'), name='products'),
    url(r'^geography/', include('geography.urls'), name='geography'),
    url(r'^activity-stream/v1/', ActivityStreamViewSet.as_view({'get': 'list'}), name='activity-stream'),
]

# to display thumbnails properly MEDIA_URL needs to have added prefix separately
urlpatterns = [
    url(r'^selling-online-overseas/', include(urlpatterns_unprefixed))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
