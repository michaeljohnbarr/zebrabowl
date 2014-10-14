from django.db import models

class GameManager(models.Manager):
    
    def active(self):
        try:
            self.last()
        except DoesNotExist:
            self.create().save()
            
        return self.last()

class Game(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    objects = GameManager()    
    class Meta:
        db_table = 'scorecard_game'    

class ScoreCardManager(models.Manager):
    """foo"""
    def active(self, game, ):
        """foo"""
        q = self.filter(game=game,).order_by('-rank', 'player_name')
        
        return  q 
    
class ScoreCard(models.Model):
    player_name = models.CharField(max_length=50L)
    game = models.ForeignKey(Game)
    total_score = models.PositiveSmallIntegerField(default = 0, )
    rank = models.PositiveSmallIntegerField(default = 0)
    objects = ScoreCardManager()
    class Meta:
        db_table = 'scorecard_card'


class FrameManager(models.Manager):
    """foo"""
    
    def make_frames(self, score_card):
        i = 1
        while i <= 10:
            """foo"""
            params = {'score_card':score_card,
                      'number':i,}
            
            self.create(**params)
            i += 1
            
        return True
        
class Frame(models.Model):
    score_card = models.ForeignKey(ScoreCard)
    number = models.PositiveSmallIntegerField()
    down_pins1 = models.PositiveSmallIntegerField(default=0)
    down_pins2 = models.PositiveSmallIntegerField(default=0)    
    is_strike = models.BooleanField(default=False)
    is_spare = models.BooleanField(default = False)
    score = models.PositiveSmallIntegerField(default=0)
    objects = FrameManager()
    class Meta:
        db_table = 'scorecard_frame'
        

            
