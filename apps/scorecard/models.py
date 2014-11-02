"""
.. module:: models.py
    :synopsis: Contains models representing key application objects, which represent aspects of a bowling game.
"""

from django.db import models
from .managers import *
import datetime
from hashlib import sha1

class Game(models.Model):
    """The game model is essentially the root model of the application, and represents 
    a bowling game"""
    
    date_created = models.DateTimeField(auto_now_add=True)
    game_hash = models.CharField(max_length=255L, unique=True,)
    objects = GameManager()    
    class Meta:
        db_table = 'scorecard_game'        

    def save(self, *args, **kwargs):
        """Overrides the save method to generate a hash based on the current
        timestamp"""
        self.game_hash = sha1(str(datetime.datetime.now())).hexdigest()
        
        super(Game, self).save(*args, **kwargs)
        
class ScoreCard(models.Model):
    """Represents a score card (i.e.player) with aggregated metrics about a player's
    performance in a game"""
    
    player_name = models.CharField(max_length=50L)
    game = models.ForeignKey(Game)
    order = models.PositiveSmallIntegerField(default = 1)
    total_score = models.PositiveSmallIntegerField(default = 0, )
    rank = models.PositiveSmallIntegerField(default = 0)
    is_active = models.BooleanField(default = False)
    objects = ScoreCardManager()
    class Meta:
        db_table = 'scorecard_card'
        
class IntegerRangeField(models.IntegerField):
    """Custom field type to support max/min integer values"""
    
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):        
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
    
            
class Frame(models.Model):
    """Represents a bowling frame, which consists of two turns per frame. A scorecard will have
    between 10 and 12 frames"""
    score_card = models.ForeignKey(ScoreCard)
    number = models.PositiveSmallIntegerField()
    down_pins1 = IntegerRangeField(default=0, max_value=10, min_value=0)
    down_pins2 = IntegerRangeField(default=0, max_value=10, min_value=0)    
    is_strike = models.BooleanField(default=False)
    is_spare = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    score = models.PositiveSmallIntegerField(default=0)
    objects = FrameManager()
    class Meta:
        db_table = 'scorecard_frame'
        ordering = ['number']