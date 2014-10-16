from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

class NewScoreCardForm(forms.ModelForm):
            
    def __init__(self, *args, **kwargs):
        super(NewScoreCardForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-scorecard-from'
        self.helper.form_class = 'horizontal-form'
        self.helper.form_action = ''
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
    class Meta:
        model = ScoreCard
        fields = ['player_name',]
    
    def save(self, game, order):
        """ Saves new score card created and returns the database object"""
        params = {'game':game,
                  'player_name':self.cleaned_data['player_name'],
                  'order':order
                  }
        
        ScoreCard.objects.create(**params).save()
        score_card = ScoreCard.objects.get(**params)
        
        return score_card
    
class BowlForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(BowlForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-bowl-from'
        self.helper.form_class = 'horizontal-form'
        self.helper.form_action = ''
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        
    class Meta:
        model = Frame
        fields = ['down_pins1','down_pins2']