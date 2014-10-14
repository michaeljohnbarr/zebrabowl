from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('apps.scorecard.views',
    url(r'^newgame/$',new_game, name='newgame'),
    url(r'^newuser/$',new_user, name='newuser'),

)
