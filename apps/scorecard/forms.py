from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

class NewScoreCardForm(forms.ModelForm):
    class Meta:
        model = ScoreCard
        fields = ['player_name',]
        
    
        
    