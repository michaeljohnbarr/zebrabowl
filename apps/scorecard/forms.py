from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

class NewScoreCardForm(forms.ModelForm):
    """A Model Form that allows users to add new score cards during initial game setup.
    This form only asks user to input the new player's name
    
    .. note:: 
        For those not familiar, this is a crispy form's implementation, which requires some of 
        the form's display logic be handled in Form.__init__(). For more info, check the docs at 
        http://django-crispy-forms.readthedocs.org/en/latest/    
    """
    
                
    def __init__(self, *args, **kwargs):
        """The initialization function wraps some Bootstrap3 classes around the form, and
        auto-adds a submit button to the form
        """
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
        """ Saves the newly-created ScoreCard object
        :param game: The current game being set up
        :type game: object
        :param order: The order the player will be in the game
        :type order: int 
        :returns: object -- Newly-created scorecard object
        """
        params = {'game':game,
                  'player_name':self.cleaned_data['player_name'],
                  'order':order
                  }
        
        ScoreCard.objects.create(**params).save()
        score_card = ScoreCard.objects.get(**params)
        
        return score_card
    
class BowlForm(forms.ModelForm):        
    """
    A model form used to record the number of pins knocked down by a player.
    """
    def __init__(self, *args, **kwargs):
        """
        Wraps Bootstrap3 classes around the form, and includes a submit button
        """
        super(BowlForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-bowl-from'
        self.helper.form_class = 'horizontal-form'
        self.helper.form_action = ''
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        
    class Meta:
        """Specifies that the frame model is used.
        Fields displayed: down_pins1, down_pins2
        """
        model = Frame
        fields = ['down_pins1','down_pins2']
    

    def clean(self):
        """
        Validates the combined of down_pins1 and down_pins2 in a frame. 
        Ensures that the total number of knocked-down pins in a frame does not
        exceed 10
        
        :param self: The form
        """
        p1 = self.cleaned_data['down_pins1']
        p2 = self.cleaned_data['down_pins2']
        
        if (p1 + p2) > 10:
            raise forms.ValidationError ("Can't knock down more than 10 pins in a frame")
        
        return self.cleaned_data
        
    def save(self, active_frame):
        """
        Save the frame form, and updates the values of the active frame.
        
        :param self: the form
        :param active_frame: The frame currently being bowled by the player
        :type active_frame: object
        :returns: object -- the updated active frame 
        """
        p1 = active_frame.down_pins1 = self.cleaned_data['down_pins1']
        p2 = active_frame.down_pins2 = self.cleaned_data['down_pins2']
        
        # determine if frame is a strike or spare
        if p1 == 10:
            active_frame.is_strike = True
        elif p1 + p2 == 10:
            active_frame.is_spare = True
                
        active_frame.is_active = False        
        active_frame.score = p1+p2                
        active_frame.save()            
        
        return active_frame