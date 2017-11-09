from django.conf import settings

from sso.utils import SSOUser, sso_api_client


class SSOUserMiddleware:

    def process_request(self, request):
        request.sso_user = None
        session_id = request.COOKIES.get(settings.SSO_PROXY_SESSION_COOKIE)

        if session_id:
            sso_response = sso_api_client.user.get_session_user(session_id)

            if sso_response.ok:
                sso_user_data = sso_response.json()
                request.sso_user = SSOUser(
                    id=sso_user_data['id'],
                    email=sso_user_data['email'],
                    session_id=session_id,
                )
