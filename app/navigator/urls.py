from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from core.views import PingView
from markets.views import HomepageView


urlpatterns = [
    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^ping\.json$', PingView.as_view(), name='ping'),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomepageView.as_view(), name='home'),
    url(r'^markets/', include('markets.urls'), name="markets"),
    url(r'^products/', include('products.urls'), name="products"),
    url(r'^geography/', include('geography.urls'), name="geography"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
