from django import forms
from .models import *

class NewUserForm(forms.ModelForm):
    class Meta:
        model = User
        
class NewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        exclude = ['date_created']
        
    
    
    
        