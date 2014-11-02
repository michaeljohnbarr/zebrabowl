from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('apps.scorecard.views',
    url(r'^home/$', new_game, name='home'),
    url(r'^newgame/$', new_game, name='newgame'),
    url(r'^newgame/(?P<username>[\w]+)/players/$', add_players, name='addplayers'),
    url(r'^gameboard/(?P<username>[\w]+)/$', game_board, name='gameboard'),
    url(r'^gamestats/$', game_stats, name='gamestats')
)
