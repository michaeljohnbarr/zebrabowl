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
    def players(self, game, ):
        """foo"""
        q = self.filter(game=game,).order_by('order', 'player_name')
        
        return  q
          
    
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
    
    def calculate_frames(self, active_frame):
        """foo"""
        
        qs = self.filter(score_card = active_frame.score_card).order_by('number')
        
        
        # calc total score of the frames to pass to ScoreCard
        ts = 0
        for i, frame1 in enumerate(qs):
            score = frame1.down_pins1 + frame1.down_pins2
            if i == len(qs)-1:
                break            
            elif i == len(qs)-2:
                frame2 = qs[i+1]
                frame3 = None
            elif i < len(qs-2):                
                frame2 = qs[i+1]
                frame3 = qs[i+2]
            
            if frame1.is_strike and not frame3:
                score += frame2.down_pins1 + frame2.down_pins2
                    
            elif frame1.is_strike and frame3:
                if frame2.is_strike:
                    score += frame2.down_pins1 + frame3.down_pins1
                else:
                    score += frame2.down_pins1 + frame2.down_pins2
                
            elif frame1.is_spare:
                score += frame2.down_pins1 + frame2.down_pins2
                
            frame1.score = score
            frame1.save()
            ts += score
        # instead of using signal, just going to manually call ScoreCard's method 
        # to update its score. can get to scorecard through any of frames in the queryset,
        # so the index used below is arbitrary
        sc = qs[0].score_card
        sc.total_score = ts
        sc.save()
        

        return qs
                    
        
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
        

            
