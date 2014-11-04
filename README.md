ZebraBowl
==========

Zebra Bowl is a cool bowling application, much like the scoring applications you see at your local bowling alley. 
I created Zebra Bowl as part of a developer test for a technology company, and have continued to iterate on the application
so prospective employers and clients can evaluate my coding abilities.

Feel free to puruse the source code, as well as check out the [documentation](http://zebrabowl.readthedocs.org).   


Features
---------

- Tracks the scores of you and your friends in real time
- Review stats on each player's performance
- Secure login and user profile, integrated with Gravatar (courtesy of [Django Userena](http://django-userena.readthedocs.org/en/latest/))

Documentation
-----------------

Documentation is located at ReadTheDocs.org

[Click Here](http://zebrabowl.readthedocs.org)

Local Installation on Unix
--------------------

### Virtual Environment Setup

- cd to the application
```$ cd /path/to/zebrabowl ```
- Create a virtual environment
``` $ virtualenv env```
- activate the environment
``` source env/bin/activate```
- Install requirements via pip:
```$ pip install -r requirements.txt```

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

