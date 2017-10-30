from django.conf import settings


def hosts(request):
    hosts = {
        'SOO_HOST': settings.SOO_HOST,
        'HELP_HOST': settings.HELP_HOST,
        'SSO_HOST': settings.SSO_HOST,
        'PROFILE_HOST': settings.PROFILE_HOST
    }

    return hosts


def sso_processor(request):
    sso_host = settings.SSO_HOST
    soo_host = settings.SOO_HOST
    url = request.build_absolute_uri()
    login_url = settings.SSO_PROXY_LOGIN_URL
    return {
        'sso_is_logged_in': request.user.is_authenticated,
        'sso_login_url': '{0}?next={1}'.format(login_url, url),
        'sso_register_url': '{0}accounts/signup/'.format(sso_host),
        'sso_logout_url': '{0}accounts/logout/?next={1}'.format(sso_host, url),
        'sso_profile_url': settings.SSO_PROFILE_URL,
    }


def header_footer_context_processor(request):
    active_classes = getattr(settings, 'HEADER_FOOTER_CSS_ACTIVE_CLASSES', {})
    return {
        'header_footer_contact_us_url': settings.HEADER_FOOTER_CONTACT_US_URL,
        'header_footer_css_active_classes': active_classes,
    }
