"""
Django settings for airline project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1*8-*#h_ym2(e=&_6&j7q+f753fp3ud$a346%1y)rh_k8beu^i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'order.apps.OrderConfig',
    'aircraft.apps.AircraftConfig',
    'city.apps.CityConfig',
    'country.apps.CountryConfig',
    'unique_flight.apps.Unique_flightConfig',
    'flight.apps.FlightConfig',
    'blog.apps.BlogConfig',
    'airport.apps.AirportConfig',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CONTEXT_PROCESSORS = (
    'django.core.context_processors.csrf',
    'django.core.context_processors.media',
)

ROOT_URLCONF = 'airline.urls'

WSGI_APPLICATION = 'airline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# for Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        "NAME": "avia",
        "USER": "avia",
        "PASSWORD": "12345",
        "HOST": "localhost",
        "PORT": "",
    }
}

# If you would like all models in your project to use BigAutoField (or another type) as the default primary key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'respectourairlines@gmail.com'
EMAIL_HOST_PASSWORD = 'c75074149131c2d'
EMAIL_PORT = 587
