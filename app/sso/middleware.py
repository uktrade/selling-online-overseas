import logging

from directory_sso_api_client.client import sso_api_client
from django.conf import settings
from requests.exceptions import RequestException
from sso.utils import SSOUser


logger = logging.getLogger(__name__)


class SSOUserMiddleware:
    MESSAGE_SSO_UNREACHABLE = 'Unable to reach SSO'

    def process_request(self, request):
        request.sso_user = None
        session_id = request.COOKIES.get(settings.SSO_SESSION_COOKIE)

        if session_id:
            try:
                sso_response = sso_api_client.user.get_session_user(session_id)
            except RequestException:
                logger.error(self.MESSAGE_SSO_UNREACHABLE, exc_info=True)
            else:
                if sso_response.ok:
                    sso_user_data = sso_response.json()
                    request.sso_user = SSOUser(
                        id=sso_user_data['id'],
                        email=sso_user_data['email'],
                        session_id=session_id,
                    )
