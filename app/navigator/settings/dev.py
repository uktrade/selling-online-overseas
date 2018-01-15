from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', 'soo.trade.great']

# Local SSO urls
SOO_HOST = 'http://soo.trade.great:8008/'
SSO_HOST = 'http://sso.trade.great:8004/'
PROFILE_HOST = 'https://profile.trade.great:8006/'
SSO_PROXY_LOGIN_URL = 'http://sso.trade.great:8004/accounts/login/'
SSO_PROXY_SIGNUP_URL = 'http://sso.trade.great:8004/accounts/signup/'
SSO_PROFILE_URL = (
    'http://profile.trade.great:8006/selling-online-overseas')

GREAT_EXPORT_HOME = 'http://exred.trade.great:8007'

# EXPORTING PERSONAS
EXPORTING_NEW = 'http://exred.trade.great:8007/new'
EXPORTING_OCCASIONAL = 'http://exred.trade.great:8007/occasional'
EXPORTING_REGULAR = 'http://exred.trade.great:8007/regular'

# GUIDANCE/ARTICLE SECTIONS
GUIDANCE_MARKET_RESEARCH = 'http://exred.trade.great:8007/market-research'
GUIDANCE_CUSTOMER_INSIGHT = (
    'http://exred.trade.great:8007/customer-insight')
GUIDANCE_FINANCE = 'http://exred.trade.great:8007/finance'
GUIDANCE_BUSINESS_PLANNING = (
    'http://exred.trade.great:8007/business-planning')
GUIDANCE_GETTING_PAID = 'http://exred.trade.great:8007/getting-paid'
GUIDANCE_OPERATIONS_AND_COMPLIANCE = (
    'http://exred.trade.great:8007/operations-and-compliance')

# SERVICES
SERVICES_EXOPPS = 'http://opportunities.export.great.gov.uk'
SERVICES_FAB = 'http://buyer.trade.great:8001'
SERVICES_GET_FINANCE = 'http://exred.trade.great:8007/get-finance'
SERVICES_SOO = 'http://soo.trade.great:8008'

# INFO
INFO_TERMS_AND_CONDITIONS = (
    'http://exred.trade.great:8007/terms-and-conditions')
INFO_ABOUT = 'http://exred.trade.great:8007/about'
INFO_PRIVACY_AND_COOKIES = (
    'http://exred.trade.great:8007/privacy-and-cookies')

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
