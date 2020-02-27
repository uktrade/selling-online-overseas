from django.http import HttpResponse

import pytest
from django.urls import reverse
from django.test.client import Client
from django.contrib.auth.models import User


@pytest.fixture
def response_with_session_cookie(settings):
    settings.SESSION_COOKIE_NAME = 'session'
    response = HttpResponse()
    response.set_cookie(
        settings.SESSION_COOKIE_NAME,
        value='123',
        domain=settings.SESSION_COOKIE_DOMAIN,
        max_age=settings.SESSION_COOKIE_AGE,
    )
    return response


@pytest.fixture(autouse=False)
def admin_user():
    admin_user = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
    admin_user.is_staff = True
    admin_user.save()
    return admin_user


@pytest.fixture()
def admin_client_sso(db, admin_user):
    """A Django test client logged in as an admin user."""
    client = Client()
    client.login(username=admin_user.email, password=admin_user._password)
    return client


@pytest.mark.django_db
def test_admin_permission_middleware_authorised_with_staff(client, settings, admin_user):
    client.force_login(admin_user)
    response = client.get(reverse('authbroker_client:login'))
    assert response.status_code == 302
