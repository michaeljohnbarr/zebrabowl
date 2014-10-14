#!/bin/bash
mysql -u root << EOF
drop database if exists zebrabowl;
create database if not exists zebrabowl;
EOF

python manage.py syncdb
