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
from directory_constants.constants import urls as default_urls

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

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
    'directory_header_footer'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ip_restriction.IpWhitelister',
    'sso.middleware.SSOUserMiddleware',
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
                'directory_header_footer.context_processors.sso_processor',
                'directory_header_footer.context_processors.urls_processor',
                ('directory_header_footer.context_processors.'
                    'header_footer_context_processor')
            ],
        },
    },
]

HEADER_FOOTER_CONTACT_US_URL = os.getenv(
    'HEADER_FOOTER_CONTACT_US_URL',
    'https://contact-us.export.great.gov.uk/directory',
)

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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

CSRF_COOKIE_HTTPONLY = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'compiled_assets'),
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'fixstatic'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Media file storage
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STORAGE_CLASSES = {
    'default': 'storages.backends.s3boto3.S3Boto3Storage',
    'local': 'django.core.files.storage.FileSystemStorage',
}
STORAGE_CLASS_NAME = os.getenv('STORAGE_TYPE', 'default')
DEFAULT_FILE_STORAGE = STORAGE_CLASSES[STORAGE_CLASS_NAME]
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY')
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
SOO_HOST = os.environ.get(
    'SOO_HOST', default_urls.SERVICES_SOO)
HELP_HOST = os.environ.get(
    'HELP_HOST', default_urls.INFO_CONTACT_US_DIRECTORY)
SSO_HOST = os.environ.get('SSO_HOST', 'https://sso.trade.great.gov.uk/')
PROFILE_HOST = os.environ.get('PROFILE_HOST', 'https://profile.great.gov.uk/')
SSO_PROXY_LOGIN_URL = os.environ.get(
    'SSO_PROXY_LOGIN_URL', 'https://sso.trade.great.gov.uk/accounts/login/')
SSO_PROXY_SIGNUP_URL = os.environ.get(
    'SSO_PROXY_SIGNUP_URL', 'https://sso.trade.great.gov.uk/accounts/signup/')
SSO_PROFILE_URL = os.environ.get(
    'SSO_PROFILE_URL', 'https://profile.great.gov.uk/selling-online-overseas')

# SSO
SSO_PROXY_SIGNATURE_SECRET = os.environ.get(
    'SSO_PROXY_SIGNATURE_SECRET', 'proxy_signature_debug')
SSO_PROXY_API_CLIENT_BASE_URL = os.environ.get(
    'SSO_PROXY_API_CLIENT_BASE_URL', 'http://sso.trade.great.dev:8004/')
SSO_PROXY_LOGIN_URL = os.environ.get(
    'SSO_PROXY_LOGIN_URL', 'http://sso.trade.great.dev:8004/accounts/login/')
SSO_PROXY_LOGOUT_URL = os.environ.get(
    'SSO_PROXY_LOGOUT_URL', 'http://sso.trade.great.dev:8004/accounts/'
    'logout/?next=http://soo.trade.great.dev:8001')
SSO_PROXY_SIGNUP_URL = os.environ.get(
    'SSO_PROXY_SIGNUP_URL', 'http://sso.trade.great.dev:8004/accounts/signup/')
SSO_PROFILE_URL = os.environ.get(
    'SSO_PROFILE_URL',
    'http://profile.trade.great.dev:8006/selling-online-overseas/')
SSO_PROXY_REDIRECT_FIELD_NAME = os.environ.get(
    'SSO_PROXY_REDIRECT_FIELD_NAME', 'next')
SSO_PROXY_SESSION_COOKIE = os.environ.get(
    'SSO_PROXY_SESSION_COOKIE', 'debug_sso_session_cookie')


THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS
