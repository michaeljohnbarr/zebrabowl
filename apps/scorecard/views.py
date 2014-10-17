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
    
def game_board(request,):
    """foo"""
    
    #get the active game and all the scorecards for the game
    game = Game.objects.active()    
    scorecards = ScoreCard.objects.players(game)
    
    # must convert numeric params back to int before performing math operations!!
    # http sends numeric params as strings
    player_num = int(request.session['player_num'])
    frame_num = int(request.session['frame_num'])
        
    # pick out the active player's card from the array 
    # calculated as  order -1 b/c of index 0
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
            
            if active_frame.is_strike or active_frame.is_spare:
                if 10 <= frame_num <= 11:
                    Frame.objects.create(score_card = active_card, number=frame_num +1).save()
                else:
                    pass
                            
            Frame.objects.calculate_frames(active_frame) 
            
            # find out which player and which frame number come next in the game                       
            session_context = Frame.objects.next_player_and_frame(request, player_num, frame_num, active_card)
            
            if session_context['last_frame'] is True:
                return redirect(reverse('addplayers'))
            else:
                return redirect(reverse('gameboard'))    
    else: 
        form = BowlForm()
    
    return render(request,'gameboard.html', {'scorecards':scorecards,
                                             'form':form,
                                             })
