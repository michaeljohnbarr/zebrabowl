#!/bin/bash

dropdb zebrabowl
createdb zebrabowl
python manage.py syncdb
python manage.py check_permissions
