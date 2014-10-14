from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import *
from .forms import *

def new_game(request):
    """foo"""

    if request.method == 'POST':
        form = NewGameForm(request.POST)
        return redirect(reverse('newgame'))
     
    else:
        form = NewGameForm()
    
    return render(request,'template.html',{'form':form})

def new_user(request):
    """foo"""
    
    if request.method =='POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            return redirect(reverse('newuser'))
    
    else:
        form = NewUserForm()
        
    return render(request,'template.html',{'form':form})