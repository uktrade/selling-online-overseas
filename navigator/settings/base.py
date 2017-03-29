"""
Django settings for enav project.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import dj_database_url

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    'core',
    'markets',
    'geography',
    'products',
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
            ],
        },
    },
]

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

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'fixstatic'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

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
        'toolbar_Custom': [
            ['Format', 'Bold', 'Italic', 'Underline', 'Strike', 'RemoveFormat'],
            ['BulletedList', 'NumberedList'],
            ['Link', 'Unlink'],
            ['Source']
        ]
    },
}

# Hosts for various services, used in templates
SOO_HOST = os.environ.get('SOO_HOST', 'https://selling-online-overseas.export.great.gov.uk/')
HELP_HOST = os.environ.get('HELP_HOST', 'https://contact-us.export.great.gov.uk/')
SSO_HOST = os.environ.get('SSO_HOST', 'https://sso.trade.great.gov.uk/')
PROFILE_HOST = os.environ.get('PROFILE_HOST', 'https://profile.great.gov.uk/')
