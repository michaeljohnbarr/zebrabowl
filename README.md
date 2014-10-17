ZebraBowl
==========

Zebra Bowl is a cool bowling scorecard!


Local Installation on Unix
--------------------

### Virtual Environment Setup

- cd to the application
'''$ cd /path/to/zebrabowl '''
- Create a virtual environment
''' $ virtualenv env'''
- activate the environment
''' source env/bin/activate'''
- make dependency installation script executable:
''' $ chmod ug+x sbin/mkenv.sh '''
- run dependency installation script
''' $ ./sbin/mkenv.sh '''

*(the mkenv script is a more fail-safe way to install dependencies)*


### Database Access and Syncdb

**If your local MySQL installation allows root access without a passowrd:**

- Make nukedb script executable
''' chmod ug+x ./sbin/nukedb.sh '''
- Run nukedb script
''' $ ./sbin/nukedb.sh '''

**Otherwise...**

- Modify mysql database settings in the django setting module
- Then, run:
'''$ python manage.py syncdb '''


**If you don't have MySQL installed**

- Change Django settings module to use the Django.db.backends.sqlite.
- run syncdb
'''$ python ./manage.py syncdb''' 
 

