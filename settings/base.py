"""
Django settings for zebrabowl project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEFAULT_INDEX_TABLESPACE = ''

SECRET_KEY = '^=!2f^ywtf9^mdoah#o_=@5q=z=x$gl#886-l9g-ujn-rqvoq4'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

############################ DATABASES ###############################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'zebrabowl',                         
        'USER': 'scott',
        'PASSWORD': 'pass',
        'HOST': 'localhost',                 
        'PORT': '',                      
    }
}

############################# EMAIL #####################################

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/home/scott/Documents/zebrabowl/app-messages'
EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'

############################# APPS ######################################

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'crispy_forms',
    'userena',
    'guardian',
    'easy_thumbnails',
    'accounts',
    'apps.scorecard',
)

########################## USERENA ###################################

USERENA_SIGNIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'
USERENA_WITHOUT_USERNAMES = True
USERENA_ACTIVATION_REQUIRED = True
######################### AUTHENTICATION ##################################

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

ANONYMOUS_USER_ID = -1

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)


############################################################################

CRISPY_TEMPLATE_PACK = 'bootstrap3'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'zebrabowl.urls'

WSGI_APPLICATION = 'apache.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

######################## STATIC #######################
STATIC_ROOT = os.path.join(os.path.dirname(__file__),'../staticcol').replace('\\','/')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(__file__),'../zebrabowl/static').replace('\\','/'),    
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

######################## TEMPLATES #######################

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'accounts.context_processors.profile',
)
TEMPLATE_DIRS = (
    #always use absolute URLs
    os.path.join(os.path.dirname(__file__),'../templates').replace('\\','/'),    
)

######################## SITES #######################
SITE_ID = 1
BASE_URL = 'localhost'

######################## URL CONFS #######################
ROOT_URLCONF = 'zebrabowl.urls'
SUBDOMAIN_URLCONFS = {
                      
}

