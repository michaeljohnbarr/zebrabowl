from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('apps.scorecard.views',
    url(r'^home/$',new_game, name='home'),
    url(r'^newgame/$',new_game, name='newgame'),
    url(r'^newgame/players/$',add_players, name='addplayers'),
    url(r'^gameboard/(?P<player_num>[0-9]+)/(?P<frame_num>[0-9]+)$',game_board, name='gameboard'),

)
