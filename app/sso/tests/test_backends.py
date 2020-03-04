from unittest import mock

from directory_sso_api_client import sso_api_client
import pytest
import requests

from django.contrib.auth import authenticate

from sso import models
from sso.tests.helpers import create_response


@pytest.fixture
def sso_request(rf, settings, client):
    request = rf.get('/')
    request.COOKIES[settings.SSO_SESSION_COOKIE] = '123'
    request.session = client.session
    return request


@pytest.mark.django_db
@mock.patch.object(sso_api_client.user, 'get_session_user', wraps=sso_api_client.user.get_session_user)
def test_auth_ok(mock_get_session_user, sso_request, settings):
    settings.AUTHENTICATION_BACKENDS = ['sso.backends.BusinessSSOUserBackend']

    mock_get_session_user.return_value = create_response({
        'id': 1,
        'email': 'jim@example.com',
        'hashed_uuid': 'thing',
        'user_profile': {
            'first_name': 'Jim',
            'last_name': 'Bloggs',
            'job_title': 'Dev',
            'mobile_phone_number': '555'
        }
    })

    user = authenticate(sso_request)

    assert isinstance(user, models.BusinessSSOUser)
    assert user.pk == 1
    assert user.id == 1
    assert user.email == 'jim@example.com'
    assert user.hashed_uuid == 'thing'
    assert user.first_name == 'Jim'
    assert user.last_name == 'Bloggs'
    assert user.job_title == 'Dev'
    assert user.mobile_phone_number == '555'
