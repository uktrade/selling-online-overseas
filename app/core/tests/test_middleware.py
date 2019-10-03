import sys
from importlib import import_module, reload
import pytest

from django.conf import settings
from django.urls import reverse, clear_url_caches
from django.contrib.auth.models import User

SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES = [
    'core.middleware.AdminPermissionCheckMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]


def reload_urlconf():
    clear_url_caches()
    reload_module(settings.ROOT_URLCONF)


def reload_module(module):
    if module in sys.modules:
        reload(sys.modules[module])
    else:
        import_module(module)


@pytest.fixture(autouse=False)
def admin_user():
    admin_user = User.objects.create_user('admin', 'admin@test.com', 'pass')
    admin_user.save()
    admin_user.is_staff = False
    admin_user.save()
    return admin_user


@pytest.mark.django_db
def test_authenticated_user_middleware_no_user(client, settings):
    settings.MIDDLEWARE_CLASSES = SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES
    settings.FEATURE_ENFORCE_STAFF_SSO_ENABLED = True
    reload_urlconf()
    response = client.get(reverse('admin:login'))

    assert response.status_code == 302
    assert response.url == reverse('authbroker_client:login')


@pytest.mark.django_db
def test_authenticated_user_middleware_authorised_no_staff(client, settings, admin_user):
    settings.MIDDLEWARE_CLASSES = SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES
    settings.FEATURE_ENFORCE_STAFF_SSO_ENABLED = True
    reload_urlconf()
    client.force_login(admin_user)

    response = client.get(reverse('admin:login'))

    assert response.status_code == 401


@pytest.mark.django_db
def test_authenticated_user_middleware_authorised_with_staff(client, settings, admin_user):
    settings.MIDDLEWARE_CLASSES = SIGNATURE_CHECK_REQUIRED_MIDDLEWARE_CLASSES
    settings.FEATURE_ENFORCE_STAFF_SSO_ENABLED = True
    reload_urlconf()
    admin_user.is_staff = True
    admin_user.save()
    client.force_login(admin_user)
    response = client.get(reverse('admin:login'))

    assert response.status_code == 302
