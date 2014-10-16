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
    
    #get the active game and the scorecards
    game = Game.objects.active()    
    scorecards = ScoreCard.objects.players(game)
    last_frame=False 
    
    # must convert back to int before performing math operations!!
    player_num = int(player_num)
    frame_num = int(frame_num)
    #pick out the active player's card from the array 
    # calculated as  order -1 b/c of index 0
    active_card = scorecards[player_num-1]
    
    active_frame = Frame.objects.get(score_card = active_card, number=frame_num)
    active_frame.is_active = True 
    active_frame.save()
      
    #handle a variety of cases depnding on what frame and who's turn it is
    if player_num < len(scorecards) and frame_num <= 10:
        player_num += 1        
        
    elif player_num == len(scorecards) and frame_num < 10:
        player_num = 1 
        frame_num += 1
    
    elif player_num == len(scorecards) and frame_num == 10:
        last_frame = True
  
    if request.method == 'POST':
        form = BowlForm(request.POST)
        if form.is_valid():
            form.save(active_frame)
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
