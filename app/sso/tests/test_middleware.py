from unittest.mock import patch, Mock


def api_response_ok(*args, **kwargs):
    return Mock(
        ok=True,
        json=lambda: {
            'id': 1,
            'email': 'jim@example.com',
        }
    )


def api_response_bad():
    return Mock(ok=False)


def test_sso_middleware_installed(settings):
    assert 'sso.middleware.SSOUserMiddleware' in settings.MIDDLEWARE_CLASSES


@patch('sso.utils.sso_api_client.user.get_session_user')
def test_sso_middleware_no_cookie(mock_get_session_user, settings, client):
    settings.MIDDLEWARE_CLASSES = ['sso.middleware.SSOUserMiddleware']
    response = client.get('/')

    mock_get_session_user.assert_not_called()
    assert response._request.sso_user is None


@patch('sso.utils.sso_api_client.user.get_session_user')
def test_sso_middleware_api_response_ok(
    mock_get_session_user, settings, client
):
    mock_get_session_user.return_value = api_response_ok()
    client.cookies[settings.SSO_PROXY_SESSION_COOKIE] = '123'
    settings.MIDDLEWARE_CLASSES = ['sso.middleware.SSOUserMiddleware']
    response = client.get('/')

    mock_get_session_user.assert_called_with('123')
    assert response._request.sso_user.id == 1
    assert response._request.sso_user.session_id == '123'
    assert response._request.sso_user.email == 'jim@example.com'


@patch('sso.utils.sso_api_client.user.get_session_user', api_response_bad)
def test_sso_middleware_bad_response(settings, client):
    settings.MIDDLEWARE_CLASSES = ['sso.middleware.SSOUserMiddleware']
    response = client.get('/')

    assert response._request.sso_user is None
