from django.db import models
from .managers import *

class Game(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    objects = GameManager()    
    class Meta:
        db_table = 'scorecard_game'    
    
    
class ScoreCard(models.Model):
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
