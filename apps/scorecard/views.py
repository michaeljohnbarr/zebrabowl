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
    scorecards = ScoreCard.objects.active(game) 
    
    if request.method == 'POST':
        form = NewScoreCardForm(request.POST)
        if form.is_valid():
            score_card =  form.save(game)
            Frame.objects.make_frames(score_card)      
            return redirect(reverse('addplayers'))
     
    else:
        form = NewScoreCardForm()        
    
    return render(request,'addplayers.html',{'form':form,
                                          'scorecards':scorecards})
    
def game_board(request):
    """foo"""
    
    game = Game.objects.active()
    scorecards = ScoreCard.objects.active(game)
    
    return render(request,'gameboard.html', {'scorecards':scorecards,})
