from django.test import override_settings, RequestFactory

from sso import context_processors


@override_settings(
    SSO_PROXY_SIGNUP_URL='http://signup.com',
    SSO_PROXY_LOGOUT_URL='http://logout.com',
    SSO_PROFILE_URL='http://profile.com',
    SSO_PROXY_LOGIN_URL='http://login.com',
)
def test_context_processor():
    request = RequestFactory().get('/')
    actual = context_processors.sso_processor(request)
    assert actual == {
        'sso_login_url': 'http://logout.com?next=/',
        'sso_register_url': 'http://signup.com',
        'sso_logout_url': 'http://logout.com',
        'sso_profile_url': 'http://profile.com',
    }
