ZebraBowl
==========

Zebra Bowl is a cool bowling scorecard!


Local Installation on Unix
--------------------

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
 
### Static Files

```$ python manage.py collectstatic```
### Start the Development Server
- at the command prompt:
``` $ python manage.py runserver```

- navigate to http://localhost:8000

- The application should be running!

