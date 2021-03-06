from .base import *

WSGI_APPLICATION = 'apache.wsgi.application'

DEBUG = True

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

# EMAIL_BACKEND = 'bandit.backends.smtp.HijackSMTPBackend'
EMAIL_BACKEND =  'django.core.mail.backends.smtp.EmailBackend'
#BANDIT_EMAIL = 'scott@scottcrespo.com'
#EMAIL_FILE_PATH = False

STATIC_ROOT = '/var/www/zebrabowl/static'
MEDIA_ROOT = '/var/www/zebrabowl/media'

#INSTALLED_APPS += (
#        'bandit',
#)

USERENA_ACTIVATION_REQUIRED = False
USERENA_SIGNIN_AFTER_SIGNUP = True