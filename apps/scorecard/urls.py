from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('apps.scorecard.views',
    url(r'^newgame/$',newgame, name='newgame'),
    url(r'^current-game/$',scorecard,name'scorecard'),

)
