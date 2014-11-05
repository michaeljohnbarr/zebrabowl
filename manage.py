#!/usr/bin/env python
import os
import sys
import socket

if __name__ == "__main__":
    
    hostname = socket.gethostname()
    
    if hostname == "highcorner1":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.base")
        
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
