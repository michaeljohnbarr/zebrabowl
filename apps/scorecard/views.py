"""
.. module:: views.py
    :Synopsis: The applications primary views

"""
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .decorators import session_required, new_game_session
from hashlib import sha1
from guardian.decorators import permission_required
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth.models import User

@login_required
@new_game_session
def new_game(request):
    """Creates a new game object in the database
    that is ready to be populated with players.    
    """    
    g = Game.objects.create()
    g.save()
    request.session['game_hash'] = g.game_hash              
    
    return render(request,'newgame.html')

@login_required
def add_players(request, username ):
    """View that enables users to enter the players of the game.
    An infinite number of players can be added to the game. once at least one player
    is added to the game, the game is ready to start."""
    
    game = Game.objects.active(request)
    scorecards = ScoreCard.objects.players(game) 
    
    if request.method == 'POST':
        form = NewScoreCardForm(request.POST)
        if form.is_valid():
            score_card =  form.save(game, len(scorecards)+1)
            Frame.objects.make_frames(score_card)      
            return redirect(reverse('addplayers', kwargs={'username':username}))
     
    else:
        form = NewScoreCardForm()        
    
    return render(request,'addplayers.html',{'form':form,
                                             'scorecards':scorecards
                                             })

@login_required
@session_required
def game_board(request, username):
    """The Game Board view is the primary view for the application. It dislpays player's
    scores for each frame and tallies up their total game score. This view also highlights which player
    and frame are active and ready to bowl."""
    
    #get the active game and all the scorecards for the game
    game = Game.objects.active(request)    
    scorecards = ScoreCard.objects.players(game)
    
    # get the current player and frame from the session
    player_num = int(request.session['player_num'])
    frame_num = int(request.session['frame_num'])
        
    # pick out the active player's card from the array 
    # calculated as  player_num -1 b/c of index 0
    active_card = scorecards[player_num-1]
    
    # retrieve the requested frame from the db and mark it as active
    active_frame = Frame.objects.get(score_card = active_card, number=frame_num)
    active_frame.is_active = True
    active_frame.save()
  
    if request.method == 'POST':
        
        form = BowlForm(request.POST,)
        
        if form.is_valid():
            active_frame = form.save(active_frame)
            
            # if there's a strike or a spare in the 10th frame, we'll have to create
            # a bonus frame to calculate the final score            
            if active_frame.number == 10 or active_frame.number == 11:
                if active_frame.is_strike:
                    Frame.objects.create_bonus_frame(request, active_frame, active_card)
                elif active_frame.is_spare:
                    if active_frame.number == 10:
                        Frame.objects.create_bonus_frame(request, active_frame, active_card)
                                            
            Frame.objects.calculate_frames(active_frame) 
            
            # find out which player and which frame number come next in the game
            player_count = ScoreCard.objects.player_count(game)                       
            session_context = Frame.objects.next_player_and_frame(request, player_count, active_card)
            
            if session_context['last_frame'] is True:
                # calculate the rankings 
                ScoreCard.objects.calc_rankings(game)                
                return redirect(reverse('gamestats'))
            
            else:
                return redirect(reverse('gameboard', kwargs={'username':username}))    
    else: 
        form = BowlForm()
    
    return render(request,'gameboard.html', {'scorecards':scorecards,
                                             'form':form,
                                             })
@login_required
@session_required    
def game_stats(request):
    """
    Displays final score and rankings for the game that just completed.
    """
    
    scorecards = ScoreCard.objects.player_ranking(
                                                  Game.objects.active(request)
                                                  )
    # flush the current session
    return render(request,'gamestats.html',{'scorecards':scorecards})
        
