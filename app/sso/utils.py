from collections import namedtuple

from django.conf import settings
from django.http import HttpResponseRedirect, QueryDict
from django.utils.six.moves.urllib.parse import urlparse, urlunparse
from django.shortcuts import resolve_url


SSOUser = namedtuple('SSOUser', ['id', 'email', 'session_id'])


class SSOAccountStateRequiredMixin:
    """ CBV mixin which verifies sso user """

    sso_redirect_url = None

    def dispatch(self, request, *args, **kwargs):
        if request.sso_user is None:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return self.redirect_to_sso(
            next_url=self.request.build_absolute_uri(),
        )

    def redirect_to_sso(self, next_url):
        """
        Redirects the user to the sso signup page, passing the 'next' page
        """
        url = build_url_with_next(
            redirect_url=self.sso_redirect_url, next_url=next_url
        )
        return HttpResponseRedirect(url)


class SSOLoginRequiredMixin(SSOAccountStateRequiredMixin):
    sso_redirect_url = settings.SSO_PROXY_LOGIN_URL


class SSOSignUpRequiredMixin(SSOAccountStateRequiredMixin):
    sso_redirect_url = settings.SSO_PROXY_SIGNUP_URL


def build_url_with_next(redirect_url, next_url):
    resolved_url = resolve_url(redirect_url)
    login_url_parts = list(urlparse(resolved_url))
    querystring = QueryDict(login_url_parts[4], mutable=True)
    querystring[settings.SSO_PROXY_REDIRECT_FIELD_NAME] = next_url
    login_url_parts[4] = querystring.urlencode(safe='/')
    return urlunparse(login_url_parts)
