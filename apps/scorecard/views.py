from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import *
from .forms import *

def new_game(request):
    """foo"""

    if request.method == 'POST':
        form = NewScoreCardForm(request.POST)
        return redirect(reverse('newgame'))
     
    else:
        form = NewScoreCardForm()
    
    return render(request,'newgame.html',{'form':form})

