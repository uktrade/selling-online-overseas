from django.conf import settings


def sso_processor(request):
    url = request.build_absolute_uri()
    login_url = settings.SSO_PROXY_LOGIN_URL
    return {
        'sso_login_url': '{0}?next={1}'.format(login_url, url),
        'sso_register_url': settings.SSO_PROXY_SIGNUP_URL,
        'sso_logout_url': settings.SSO_PROXY_LOGOUT_URL,
        'sso_profile_url': settings.SSO_PROFILE_URL,
    }
