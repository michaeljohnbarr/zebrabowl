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
    
class BowlForm(forms.Form):
    
    down_pins1 = forms.IntegerField(required = True, max_value = 10, min_value=0,)
    down_pins2 = forms.IntegerField(required = True, max_value = 10, min_value=0,)
    
    
    def __init__(self, *args, **kwargs):
        super(BowlForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-bowl-from'
        self.helper.form_class = 'horizontal-form'
        self.helper.form_action = ''
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        
        
    def clean(self):

        try: 
            self.cleaned_data['down_pins1']
            self.cleaned_data['down_pins2']
        except KeyError:
            raise forms.ValidationError("you need to enter values for both fields")        
        else:
            p1 = self.cleaned_data['down_pins1']
            p2 = self.cleaned_data['down_pins2']
        if (p1 + p2) > 10:
            raise forms.ValidationError ("Can't knock down more than 10 pins in a frame")
        
        return p1, p2
 
    
    def save(self, active_frame):
        
        active_frame.down_pins1 = self.cleaned_data[0]
        active_frame.down_pins2 = self.cleaned_data[1]
        active_frame.is_active = False
        
        active_frame.save()
        
        return active_frame
        
        
        