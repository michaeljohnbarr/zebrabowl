#!/bin/bash

rm zebrabowldb
python manage.py syncdb
