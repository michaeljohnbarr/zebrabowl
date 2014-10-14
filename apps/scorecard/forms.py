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
    
    def save(self, game):
        
        mydict = {'game':game,
                  'player_name':self.cleaned_data['player_name']}
        
        return ScoreCard.objects.create(**mydict).save()