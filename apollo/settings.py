"""
Django settings for apollo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ON_PAAS = 'OPENSHIFT_REPO_DIR' in os.environ

if ON_PAAS:
    SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']
else:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = ')_7av^!cy(wfx=k#3*7x+(=j^fzv+ot^1@sh9s9t=8$bu@r(z$'

# SECURITY WARNING: don't run with debug turned on in production!
# adjust to turn off when on Openshift, but allow an environment variable to override on PAAS
DEBUG = not ON_PAAS
DEBUG = DEBUG or 'DEBUG' in os.environ
if ON_PAAS and DEBUG:
    print("*** Warning - Debug mode is on ***")

TEMPLATE_DEBUG = True

if ON_PAAS:
    ALLOWED_HOSTS = [os.environ['OPENSHIFT_APP_DNS'], socket.gethostname(), 'apollo.alexander-wong.com', ]
else:
    ALLOWED_HOSTS = []

# Application definition

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    "django.contrib.sites",
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Internally Installed Applications
    'apps.business',
    'apps.assets',
    'apps.price_list',
    'apps.station',
    'apps.terms_of_service',
    # Externally Installed Applications
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrap3',
    'cities_light',
    'djangular',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'apollo.urls'

SITE_ID = 1

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

WSGI_APPLICATION = 'apollo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if ON_PAAS:
    # determine if we are on MySQL or POSTGRESQL
    if "OPENSHIFT_MYSQL_DB_USERNAME" in os.environ:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ['OPENSHIFT_APP_NAME'],
                'USER': os.environ['OPENSHIFT_MYSQL_DB_USERNAME'],
                'PASSWORD': os.environ['OPENSHIFT_MYSQL_DB_PASSWORD'],
                'HOST': os.environ['OPENSHIFT_MYSQL_DB_HOST'],
                'PORT': os.environ['OPENSHIFT_MYSQL_DB_PORT'],
            }
        }
    elif "OPENSHIFT_POSTGRESQL_DB_USERNAME" in os.environ:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': os.environ['OPENSHIFT_APP_NAME'],
                'USER': os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME'],
                'PASSWORD': os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD'],
                'HOST': os.environ['OPENSHIFT_POSTGRESQL_DB_HOST'],
                'PORT': os.environ['OPENSHIFT_POSTGRESQL_DB_PORT'],
            }
        }

else:
    # stock django, local development.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATIC_ROOT = os.path.join(BASE_DIR, "wsgi", "static")
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "static"),
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

# Email & Django All Auth Email Permissions
# https://docs.djangoproject.com/en/1.7/topics/email/
ACCOUNT_EMAIL_REQUIRED = True
ADMINS = (
    ('Alexander Wong', 'admin@alexander-wong.com'),
)
if ON_PAAS:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ['OPENSHIFT_EMAIL_HOST']
    EMAIL_PORT = os.environ['OPENSHIFT_EMAIL_PORT']
    EMAIL_HOST_USER = os.environ['OPENSHIFT_EMAIL_HOST_USER']
    EMAIL_HOST_PASSWORD = os.environ['OPENSHIFT_EMAIL_HOST_PASSWORD']
    EMAIL_SUBJECT_PREFIX = '[Apollo] '
    DEFAULT_FROM_EMAIL = os.environ['OPENSHIFT_DEFAULT_FROM_EMAIL']
    EMAIL_USE_TLS = True
    ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    ACCOUNT_EMAIL_SUBJECT_PREFIX = EMAIL_SUBJECT_PREFIX
else:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
    ACCOUNT_EMAIL_VERIFICATION = "none"

LOGIN_REDIRECT_URL = '/'

# Django REST Framework Settings
REST_FRAMEWORK = {
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# Django Cities Light Settings
TRANSLATION_LANGUAGES = ['en']

# Django Guardian Settings
ANONYMOUS_USER_ID = -1
GUARDIAN_RAISE_403 = True