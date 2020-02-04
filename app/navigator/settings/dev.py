from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Local SSO urls
SOO_HOST = 'http://soo.trade.great:8008/'
HELP_HOST = 'http://contact.trade.great:8009/'
SSO_HOST = 'http://sso.trade.great:8004/'
PROFILE_HOST = 'https://profile.trade.great:8006/'
SSO_PROXY_LOGIN_URL = 'http://sso.trade.great:8004/accounts/login/'
SSO_PROXY_SIGNUP_URL = 'http://sso.trade.great:8004/accounts/signup/'
SSO_PROFILE_URL = (
    'http://profile.trade.great:8006/selling-online-overseas')

HEADER_FOOTER_URLS_GREAT_HOME = "http://exred.trade.great:8007/"
HEADER_FOOTER_URLS_FAB = "http://buyer.trade.great:8001"
HEADER_FOOTER_URLS_SOO = "/"
HEADER_FOOTER_URLS_CONTACT_US = "http://contact.trade.great:8009/directory/"

# SSO
SSO_PROXY_SIGNATURE_SECRET = 'proxy_signature_debug'
SSO_PROXY_API_CLIENT_BASE_URL = 'http://sso.trade.great:8004/'
SSO_PROXY_LOGIN_URL = 'http://sso.trade.great:8004/accounts/login/'
SSO_PROXY_LOGOUT_URL = (
    'http://sso.trade.great:8004/accounts/logout/'
    '?next=http://soo.trade.great:8008')
SSO_PROXY_SIGNUP_URL = 'http://sso.trade.great:8004/accounts/signup/'
SSO_PROFILE_URL = (
    'http://profile.trade.great:8006/selling-online-overseas/')
SSO_PROXY_REDIRECT_FIELD_NAME = 'next'
SSO_PROXY_SESSION_COOKIE = 'debug_sso_session_cookie'
