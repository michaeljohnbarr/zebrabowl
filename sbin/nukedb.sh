#!/bin/bash

dropdb zebrabowl
createdb zebrabowl
python manage.py syncdb
