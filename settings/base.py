# Django settings for localized_classified_ads project.
import os
import sys

OVERWRITE_EXTENDS = True

INTERNAL_IPS = ('127.0.0.1',)

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ADMINS = (
    ('sam', 'samuel.goldszmidt@gmail.com'),
)

MODERATORS = ('contact@achetersanscom.com', )
DJANGO_MODERATION_MODERATORS = MODERATORS
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'achetersanscom_db',                      # Or path to database file if using sqlite3.
        'USER': 'achetersanscom',                      # Not used with sqlite3.
        'PASSWORD': 'admin',                  # Not used with sqlite3.
        'HOST': 'postgresql.alwaysdata.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

BYPASS_GEOCODE = False
GEOCODE = 'nominatim'
#from django.contrib.sites.models import Site
#current_site = Site.objects.get_current()
#print current_site

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-FR'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'public', 'media')
STATIC_DOC_ROOT = MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"

STATIC_URL = '/static/'
STATIC_ROOT = '/home/achetersanscom/localized_classified_ads/public/static'
#STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(SITE_ROOT, 'static'),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@#%3165dp3&jyggru=jt38%vs&d=!u)@*xrhg!o8n+%sd6m^1h'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    #'johnny.middleware.LocalStoreClearMiddleware',
    #'johnny.middleware.QueryCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_sorting.middleware.SortingMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dynamicsites.middleware.DynamicSitesMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'dynamicsites.context_processors.current_site',
    'django.core.context_processors.request',
    'context_processors.localized_classified_ads_context_processor',
    'context_processors.google_analytics_context_processor',
    'context_processors.site_specific_styles'
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'localized_classified_ads.urls'
#ROOT_URLCONF= 'localized_classified_ads.sites.achetersanscom.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'django.contrib.flatpages',
    'django.contrib.sitemaps',
    #'easy_thumbnails',
    'profiles',
    'guardian',
    'south',
    'userena',
    'django_sorting',
    'floppyforms',
    'form_utils',
    'crispy_forms',
    'django_filters',
    #'ads',
    'geoads',
    'pagination',
    'moderation',
    'utils',
    #'mockups',
    'debug_toolbar',
    'dynamicsites',
    'compressor',
    'sites.achetersanscom.ads',
    'sites.louersanscom.ads',
    #'smartextends',
    'raven.contrib.django',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


EMAIL_HOST = "smtp.alwaysdata.com"
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = "contact@achetersanscom.com"
EMAIL_HOST_USER = "achetersanscom@alwaysdata.net"
EMAIL_HOST_PASSWORD = "Sam25sn06"

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'profiles.UserProfile'

LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
#LOGOUT_URL = '/'

# below settings needed by ads app
ADS_PROFILE_URL = '/accounts/%s/'
ADS_PROFILE_SIGNUP = '/accounts/signup/'

USERENA_WITHOUT_USERNAMES = True
USERENA_DISABLE_PROFILE_LIST = True

# TWITTER

TWITTER_NOTIFICATION = True

TWITTER_CONSUMER_KEY = 'vRAok6pEjJxWFL9Pbtzfg'
TWITTER_CONSUMER_SECRET = 'DOg8Gu0F3udkLTHj2nLI1Vxg2VFHbVd4TVgux7A'
TWITTER_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
TWITTER_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
TWITTER_AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
TWITTER_ACCESS_TOKEN_KEY = '163195482-oSknQtcXYPue5iclWAw85pV34gSxvVXODhOHVT3O'
TWITTER_ACCESS_TOKEN_SECRET = 'JxxAIHq8w39hV6vAkLWy7V2gPetQ8KOzrQIhv1pvo'

SITES_DIR = os.path.join(os.path.dirname(__file__), 'sites')
DEFAULT_HOST = 'achetersanscom.com'

HOSTNAME_REDIRECTS = {
    #'www.louersanscom.com':'louersanscom.com',
    #'www.achetersanscom.com':'achetersanscom.com'
}

GEOIP_PATH = '/home/achetersanscom/geoip'


# sites specific model, form, filter configurations

# PER_SITE_OBJECTS = {}

GOOGLE_ANALYTICS_ACCOUNTS = {'achetersanscom.com':{'DomainName':'achetersanscom.com', 'Account':'UA-17174958-2'}, 
                             'louersanscom.com':{'DomainName':'louersanscom.com', 'Account':'UA-17174958-3'}}

SITE_SPECIFIC_STYLES = {
    'achetersanscom.com':{'SPECIFIC_STYLE':'css/achetersanscom.css'},
    'louersanscom.com':{'SPECIFIC_STYLE':'css/louersanscom.css'}
}

SENTRY_DSN = 'https://c3ee02a9760d40f795c6c9355ac76ab3:8ffd8927be8449e28e9f831c8424fdef@app.getsentry.com/170'

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

