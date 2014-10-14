from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)    
    
    class Meta:
        db_table = 'scorecard_game'    
    
class ScoreCard(models.Model):
    user = models.ManyToManyField(User)
    game = models.ForeignKey(Game)
    total_score = models.PositiveSmallIntegerField(default = 0, )
    rank = models.PositiveSmallIntegerField(blank=True )
    
    class Meta:
        db_table = 'scorecard_card'

class Frame(models.Model):
    score_card = models.ForeignKey(ScoreCard)
    number = models.PositiveSmallIntegerField(min_value = 1, max_value = 10)
    down_pins1 = models.PositiveSmallIntegerField(min_value=0, max_value = 10)
    down_pins2 = models.PositiveSmallIntegerField(min_value=0, max_value = 10, blank=True)    
    is_strike = models.BooleanField(default=False)
    is_spare = models.BooleanField(default = False)
    score = models.PositiveSmallIntegerField(default=0)
    class Meta:
        db_table = 'scorecard_frame'
        
