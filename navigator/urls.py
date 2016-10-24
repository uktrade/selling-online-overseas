from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls'), name="core"),
    url(r'^markets/', include('markets.urls'), name="markets"),
    url(r'^products/', include('products.urls'), name="products"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
