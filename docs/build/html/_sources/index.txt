.. ZebraBowl documentation master file, created by
   sphinx-quickstart on Sun Oct 19 15:45:12 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ZebraBowl's documentation!
=====================================

Contents:

.. toctree::
	:maxdepth: 2
   
	modules/modules.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Local Installation on Unix
===========================

### Virtual Environment Setup

- cd to the application
```$ cd /path/to/zebrabowl ```
- Create a virtual environment
``` $ virtualenv env```
- activate the environment
``` source env/bin/activate```
- make dependency installation script executable:
``` $ chmod ug+x sbin/mkenv.sh ```
- run dependency installation script
``` $ ./sbin/mkenv.sh ```

*(the mkenv script is a more fail-safe way to install dependencies)*


### Database Access and Syncdb

We're using SQLite3 for portability. To get the db running, simply enter
```$ python manage.py syncdb```
 

### Start the Development Server
- at the command prompt:
``` $ python manage.py runserver```

- navigate to http://localhost:8000

- The application should be running!



