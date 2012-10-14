#-*- coding: utf-8 -*-
from __future__ import absolute_import
from .base import *

#STATIC_ROOT = "os.path.join(SITE_ROOT, 'static')"

import os
import sys

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


sys.path.append('/Users/goldszmidt/sam/perso/dev/django-geoads')


TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'

# I exclude admin.py files from my coverage
# these files does'nt set anything spectial
COVERAGE_MODULE_EXCLUDES = ['tests$', 'settings$', 'urls$', 'locale$',
                                    'common.views.test', '__init__', 'django',
                                    'migrations', 'admin']

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(SITE_ROOT, 'coverage_report')

BYPASS_GEOCODE = False

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'achetersanscom_db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'
EMAIL_HOST_USER = ''

#CACHES = {
#    'default' : dict(
#        BACKEND = 'johnny.backends.memcached.MemcachedCache',
#        LOCATION = ['127.0.0.1:11211'],
#        JOHNNY_CACHE = True,
#    )
#}
#JOHNNY_MIDDLEWARE_KEY_PREFIX='jc_lca'

TWITTER_NOTIFICATION = False

ENV_HOSTNAMES = {
    'achetersanscom.dev': 'www.achetersanscom.com',
    'louersanscom.dev': 'www.louersanscom.com'
}

STATIC_ROOT = os.path.join(SITE_ROOT, 'static')
STATICFILES_DIRS = ()

SITES_DIR = '/Users/goldszmidt/sam/perso/dev/localized_classified_ads/sites'

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

GEOIP_PATH = '/Users/goldszmidt/sam/perso/dev/geoip'
#GEOIP_LIBRARY_PATH = '/Users/goldszmidt/sam/perso/dev/geoip'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'profiles.views': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'geoads': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'ads': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'sites.achetersanscom.ads': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'dynamicsites': {
            'handlers': ['console'],
            'level': 'ERROR',
        }
    }
}

