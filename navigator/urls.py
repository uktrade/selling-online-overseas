from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls'), name="core"),
    url(r'^contact/', include('contact.urls'), name="contact"),
    url(r'^markets/', include('markets.urls'), name="markets"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
