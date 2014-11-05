from base import *

WSGI_APPLICATION = 'apache.wsgi.application'

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zebrabowl',                         
        'USER': 'scott',
        'PASSWORD': 'DBSAFE789',
        'HOST': 'localhost',                 
        'PORT': '',                      
    }
}

BASE_URL = 'zebrabowl.scottcrespo.com'

ALLOWED_HOSTS = ['.scottcrespo.com',
                 '.localhost',
                 '.104.236.49.119',]

EMAIL_BACKEND = 'bandit.backends.smtp.HijackSMTPBackend'
BANDIT_EMAIL = 'scott@scottcrespo.com'
EMAIL_FILE_PATH = False

STATIC_ROOT = '/var/www/zebrabowl/static'
MEDIA_ROOT = '/var/www/zebrabowl/media'