"""
WSGI config for zebrabowl project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import socket
import sys

hostname = socket.gethostname()
    
if hostname == "highcorner1":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")
    sys.path.append('/home/scott/zebrabowl')
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
