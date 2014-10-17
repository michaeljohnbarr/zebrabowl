from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import *
from .forms import *

def home(request):
    """foo"""
    return render(request,'base.html')

def new_game(request):
    """foo"""

    new_game = Game.objects.create().save()              
    
    return render(request,'newgame.html')


def add_players(request):
    """Foo"""
    
    game = Game.objects.active()
    scorecards = ScoreCard.objects.players(game) 
    
    if request.method == 'POST':
        form = NewScoreCardForm(request.POST)
        if form.is_valid():
            score_card =  form.save(game, len(scorecards)+1)
            Frame.objects.make_frames(score_card)      
            return redirect(reverse('addplayers'))
     
    else:
        form = NewScoreCardForm()        
    
    return render(request,'addplayers.html',{'form':form,
                                             'scorecards':scorecards
                                             })
    
def game_board(request, player_num, frame_num):
    """foo"""
    
    #get the active game and all the scorecards for the game
    game = Game.objects.active()    
    scorecards = ScoreCard.objects.players(game)
    player_count = len(scorecards)
    
    # last frame is false until proven otherwise
    last_frame=False 
    
    # must convert numeric params back to int before performing math operations!!
    # http sends numeric params as strings
    player_num = int(player_num)
    frame_num = int(frame_num)
    
    #pick out the active player's card from the array 
    # calculated as  order -1 b/c of index 0
    active_card = scorecards[player_num-1]
    
    active_frame = Frame.objects.get(score_card = active_card, number=frame_num)
    active_frame.is_active = True
    active_frame.save()
  
    if request.method == 'POST':
        frame_count = Frame.objects.filter(score_card = active_card).count()
        
        #handle a variety of cases depnding on what frame it is and who's turn it is..        
        
        # it's not the last player's turn
        # incraese the player number but not the frame number 
        if player_num < player_count:
            player_num += 1        
            
        # it's the last player's turn, but not the final frame.
        # return to player 1, and increase frame num by 1
        elif player_num == player_count and frame_num < frame_count:
            player_num = 1 
            frame_num += 1
        
        # it's  the last player of the last frame. so the game is over
        elif player_num == player_count and frame_num == frame_count:
            last_frame = True
        

        form = BowlForm(request.POST,)
        
        if form.is_valid():
            active_frame = form.save(active_frame)
            
            # if there's a strike or a spare in the 10th frame, we'll have to create
            # a bonus frame to calculate the final score 
            if frame_num >= 10 and active_frame.is_strike or active_frame.is_spare:
                Frame.objects.create(score_card = active_card, number=frame_num +1).save()
            
            Frame.objects.calculate_frames(active_frame)
            
            if last_frame is True:
                return redirect(reverse('addplayers'))
            else:
                return redirect(reverse('gameboard', kwargs= {'player_num':player_num,
                                                               'frame_num':frame_num
                                                               }))    
    else: 
        form = BowlForm()
    
    return render(request,'gameboard.html', {'scorecards':scorecards,
                                             'form':form,
                                             'active_card':active_card,
                                             'active_frame':active_frame})
