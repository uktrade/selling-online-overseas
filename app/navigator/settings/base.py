"""
Django settings for enav project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

import dj_database_url
from easy_thumbnails.conf import Settings as thumbnail_settings
import environ
from django.urls import reverse_lazy

from directory_constants import cms

env = environ.Env()
env.read_env()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# Application definition

INSTALLED_APPS = [
    'grappelli',
    'reversion',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'ckeditor',
    'easy_thumbnails',
    'image_cropping',
    'core',
    'markets',
    'geography',
    'products',
    'thumber',
    'directory_components',
    'activitystream.apps.ActivityStreamConfig',
    'django_extensions',
    'authbroker_client',
]

MIDDLEWARE_CLASSES = [
    'core.middleware.AdminPermissionCheckMiddleware',
    'admin_ip_restrictor.middleware.AdminIPRestrictorMiddleware',
    'directory_components.middleware.MaintenanceModeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'sso.middleware.SSOUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'navigator.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "core", "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.hosts',
                'directory_components.context_processors.sso_processor',
                'directory_components.context_processors.urls_processor',
                'directory_components.context_processors.cookie_notice',
                ('directory_components.context_processors.'
                    'header_footer_processor'),
                'directory_components.context_processors.analytics',
                'directory_components.context_processors.feature_flags'
            ],
        },
    },
]

HEADER_FOOTER_CSS_ACTIVE_CLASSES = {'soo': True}

WSGI_APPLICATION = 'navigator.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config()
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# To enable URLs to correctly using the user facing domain

USE_X_FORWARDED_HOST = True

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', True)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_HOST = env.str('STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'compiled_assets'),
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'fixstatic'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Media file storage
MEDIA_URL = '/selling-online-overseas/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGE_CLASSES = {
    'default': 'storages.backends.s3boto3.S3Boto3Storage',
    'local': 'django.core.files.storage.FileSystemStorage',
}
STORAGE_CLASS_NAME = env.str('STORAGE_TYPE', 'default')
DEFAULT_FILE_STORAGE = STORAGE_CLASSES[STORAGE_CLASS_NAME]
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME', '')
AWS_ACCESS_KEY_ID = env.str('AWS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_KEY', '')
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False
AWS_S3_ENCRYPTION = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = 'eu-west-2'
IMAGE_CROPPING_THUMB_SIZE = (710, 537)

# Index location for Whoosh searching
WHOOSH_INDEX_DIR = os.path.join(BASE_DIR, 'whoosh_index')

DEBUG = False
SESSION_COOKIE_AGE = 43200  # 12 hours
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)

# Grappelli settings
GRAPPELLI_ADMIN_TITLE = "Selling Online Overseas CMS"

# CKEDITOR configuration
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'format_tags': 'p',
        'forcePasteAsPlainText': True,
        'disableNativeSpellChecker': False,
        'toolbar_Custom': [
            ['Format', 'Bold', 'Italic', 'Underline', 'Strike',
                'RemoveFormat'],
            ['BulletedList', 'NumberedList'],
            ['Link', 'Unlink'],
            ['Source']
        ]
    },
}

# Hosts for various services, used in templates
PROFILE_HOST = env.str('PROFILE_HOST', 'https://profile.great.gov.uk/')

# SSO API Client
DIRECTORY_SSO_API_CLIENT_BASE_URL = env.str('DIRECTORY_SSO_API_CLIENT_BASE_URL', '')
DIRECTORY_SSO_API_CLIENT_API_KEY = env.str('DIRECTORY_SSO_API_CLIENT_API_KEY', '')
DIRECTORY_SSO_API_CLIENT_SENDER_ID = env.str(
    'DIRECTORY_SSO_API_CLIENT_SENDER_ID', 'directory'
)
DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT = env.int(
    'DIRECTORY_SSO_API_CLIENT_DEFAULT_TIMEOUT', 5
)

# SSO
SSO_PROXY_SIGNATURE_SECRET = env.str(
    'SSO_PROXY_SIGNATURE_SECRET', 'proxy_signature_debug'
)
SSO_PROXY_API_CLIENT_BASE_URL = env.str(
    'SSO_PROXY_API_CLIENT_BASE_URL', ''
)
SSO_PROXY_LOGIN_URL = env.str(
    'SSO_PROXY_LOGIN_URL', ''
)
SSO_PROXY_LOGOUT_URL = env.str(
    'SSO_PROXY_LOGOUT_URL', ''
)
SSO_PROXY_SIGNUP_URL = env.str(
    'SSO_PROXY_SIGNUP_URL', ''
)
SSO_PROFILE_URL = env.str(
    'SSO_PROFILE_URL', ''
)
SSO_PROXY_REDIRECT_FIELD_NAME = env.str(
    'SSO_PROXY_REDIRECT_FIELD_NAME', 'next'
)
SSO_PROXY_SESSION_COOKIE = env.str(
    'SSO_PROXY_SESSION_COOKIE', 'debug_sso_session_cookie'
)
SSO_SESSION_COOKIE = env.str('SSO_SESSION_COOKIE')

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

# HEADER/FOOTER URLS
DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC = env.str(
    'DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC', ''
)
DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES = env.str(
    'DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES', ''
)
DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS = env.str(
    'DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS', ''
)
DIRECTORY_CONSTANTS_URL_EVENTS = env.str(
    'DIRECTORY_CONSTANTS_URL_EVENTS', ''
)
DIRECTORY_CONSTANTS_URL_INVEST = env.str('DIRECTORY_CONSTANTS_URL_INVEST', '')
DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER = env.str(
    'DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER', ''
)
DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON = env.str(
    'DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON', ''
)
DIRECTORY_CONSTANTS_URL_FIND_A_BUYER = env.str(
    'DIRECTORY_CONSTANTS_URL_FIND_A_BUYER', ''
)

# Google tag manager
GOOGLE_TAG_MANAGER_ID = env.str('GOOGLE_TAG_MANAGER_ID', 'GTM-W2J5DMC')
GOOGLE_TAG_MANAGER_ENV = env.str('GOOGLE_TAG_MANAGER_ENV', '')
UTM_COOKIE_DOMAIN = None
PRIVACY_COOKIE_DOMAIN = env.str('PRIVACY_COOKIE_DOMAIN', '')

# Admin restrictor
RESTRICT_ADMIN_BY_IPS = env.bool('RESTRICT_ADMIN_BY_IPS', False)
RESTRICT_ADMIN = RESTRICT_ADMIN_BY_IPS
ALLOWED_ADMIN_IPS = env.list('ALLOWED_ADMIN_IPS', default=[])
ALLOWED_ADMIN_IP_RANGES = env.list('ALLOWED_ADMIN_IP_RANGES', default=[])

RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN', ''),
}

# feature flags
FEATURE_FLAGS = {
    # used by directory-components
    'MAINTENANCE_MODE_ON': env.bool('FEATURE_MAINTENANCE_MODE_ENABLED', False),
    'NEW_HEADER_FOOTER_ON': env.bool(
        'FEATURE_NEW_HEADER_FOOTER_ENABLED', False
    ),
    'HEADER_SEARCH_ON': env.bool('FEATURE_HEADER_SEARCH_ENABLED', False),
    'ENFORCE_STAFF_SSO_ON': env.bool('FEATURE_ENFORCE_STAFF_SSO_ENABLED', False),
}

if FEATURE_FLAGS['ENFORCE_STAFF_SSO_ON']:
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'authbroker_client.backends.AuthbrokerBackend'
    ]
    LOGIN_URL = reverse_lazy('authbroker:login')
    LOGIN_REDIRECT_URL = reverse_lazy('admin:index')

    # authbroker config
    AUTHBROKER_URL = env.str('STAFF_SSO_AUTHBROKER_URL')
    AUTHBROKER_CLIENT_ID = env.str('AUTHBROKER_CLIENT_ID')
    AUTHBROKER_CLIENT_SECRET = env.str('AUTHBROKER_CLIENT_SECRET')


# directory CMS
DIRECTORY_CMS_API_CLIENT_BASE_URL = env.str('CMS_URL')
DIRECTORY_CMS_API_CLIENT_API_KEY = env.str('CMS_SIGNATURE_SECRET')
DIRECTORY_CMS_API_CLIENT_SENDER_ID = 'directory'
DIRECTORY_CMS_API_CLIENT_SERVICE_NAME = cms.EXPORT_READINESS
DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT = 15
DIRECTORY_CMS_SITE_ID = env.str('DIRECTORY_CMS_SITE_ID', 3)

# directory clients
DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS = env.int(
    'DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS',
    60 * 60 * 24 * 30  # 30 days
)

# Activity Stream API
ACTIVITY_STREAM_ACCESS_KEY_ID = env.str('ACTIVITY_STREAM_ACCESS_KEY_ID')
ACTIVITY_STREAM_SECRET_ACCESS_KEY = env.str('ACTIVITY_STREAM_SECRET_ACCESS_KEY')

cache = {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    'LOCATION': 'unique-snowflake',
}

CACHES = {
    'default': cache,
    'api_fallback': cache,
    'cms_fallback': cache,
}