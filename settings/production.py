from base import *

WSGI_APPLICATION = 'apache.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zebrabowl',                         
        'USER': 'scott',
        'PASSWORD': '',
        'HOST': 'localhost',                 
        'PORT': '',                      
    }
}