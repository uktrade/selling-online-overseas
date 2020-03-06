from unittest import mock

import pytest
import requests_mock

from sso.tests.helpers import create_response


@pytest.mark.django_db
@mock.patch('directory_sso_api_client.sso_api_client.user.get_session_user')
def test_authenticated(mock_get_session_user, client, settings):
    client.cookies[settings.SSO_SESSION_COOKIE] = '123'
    mock_get_session_user.return_value = create_response({'id': 1, 'email': 'jim@example.com', 'hashed_uuid': 'thing'})

    response = client.get('/')
    request = response.wsgi_request

    assert request.user.is_authenticated
    assert request.user.id == 1
    assert request.user.pk == 1
    assert request.user.email == 'jim@example.com'
    assert request.user.hashed_uuid == 'thing'


@pytest.mark.django_db
@mock.patch('directory_sso_api_client.sso_api_client.user.get_session_user')
def test_not_authenticated(mock_get_session_user, client, settings):
    client.cookies[settings.SSO_SESSION_COOKIE] = '123'

    mock_get_session_user.return_value = create_response(status_code=404)

    response = client.get('/')

    request = response.wsgi_request
    assert not request.user.is_authenticated
