import os

from django.utils.translation import gettext_lazy as _

# Include Scala settings
from ScalaApp.scala_settings import *  # noqa: F401, F403


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^nnb_o98(2#bb&346s&h=o5td#_d&nc&qkm^=wn*k*as@)=49p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'UserDetails.User'

# django.contrib.admin is replaced by ScalaApp.apps.MyAdminConfig
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'dal',
    'dal_select2',
    'ScalaApp.apps.MyAdminConfig',

    'widget_tweaks',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauthproviders.quadrivium',

    'UserDetails.apps.UserDetailsConfig',
    'Dining.apps.DiningConfig',
    'CreditManagement.apps.CreditManagementConfig',
    'General.apps.GeneralConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ScalaApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'assets/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ScalaApp.context_processors.scala'
            ],
        },
    },
    {
        'NAME': 'EmailTemplates',
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'assets/mails')],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': ['General.templatetags.mail_tags'],
        }
    },
]

WSGI_APPLICATION = 'ScalaApp.wsgi.application'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


STATIC_ROOT = os.path.join(BASE_DIR, "static_total")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets/static/'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

MEDIA_URL = "/media/"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

DATE_FORMAT = "l j F"

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Correct localization, see:
# https://docs.djangoproject.com/en/2.1/topics/i18n/translation/#how-django-discovers-language-preference
# https://docs.djangoproject.com/en/2.1/topics/i18n/formatting/
USE_THOUSAND_SEPARATOR = True
LANGUAGES = [
    ('en', _('English')),
    # ('nl', _('Dutch')),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# For debugging SQL queries, see:
# https://docs.djangoproject.com/en/2.1/ref/templates/api/#django-template-context-processors-debug
INTERNAL_IPS = ['127.0.0.1']


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

# Show e-mails in console for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Allauth configuration
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_FORMS = {
    'change_password': 'UserDetails.forms_allauth.CustomChangePasswordForm',
    'reset_password_from_key': 'UserDetails.forms_allauth.CustomResetPasswordKeyForm',
}
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
# Set to None to ask the user ("Remember me?")
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_ADAPTER = "UserDetails.externalaccounts.SocialAccountAdapter"
