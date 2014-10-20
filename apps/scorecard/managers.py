"""
.. module:: managers.py
    :Synopsis: This is where app's heavy lifing takes place

"""

from django.db import models

class GameManager(models.Manager):
    """ Provides table-level functionality to the Game model.
    """
    def active(self, request):
        """Returns the current (active) game being played. The function first attempts
        to pull the game_hash from the session. If that fails then it falls back to pulling the most-recently
        created game in the database. For a more fail-safe implementation, a better approach is
        to tie a game to a particular user and cache the game and user in the session. But, it goes beyond the
        scope of this exercise.
        
        :param request: HTTP request
        :request type: object
        """
        
        try:
            request.session['game_hash']
        except KeyError:
            active_game = self.last()
        else:
            active_game = self.get(game_hash = request.session['game_hash'])
        
        return active_game
    

class ScoreCardManager(models.Manager):
    """Provides table-level functionality to the ScoreCard model.    
    """
    def players(self, game,):
        """Returns the sorecards of all the players in the active game.
        
        :param game: The game we want the scorecards from
        :type game: object
        :returns: queryset -- a list of ScoreCard objects
        """
        query = self.filter(game=game,).order_by('order', 'player_name')
        
        return  query
    
    def player_count(self, game):
        """ 
        Returns number of players in the game.
        
        :param game: The game we want information about
        :type game: object
        :returns: int -- the number of players in the game
        """
        query = self.filter(game=game).count()
        
        return query
    
    def calc_rankings(self, game):
        """
        Calculates each player's ranking and updates players' scorecards accordingly
        
        :param game: The game we want information about
        :type game: object
        :returns: bool -- True if the function executed completely
        """

        query = self.player_ranking(game)
        
        for i, item in enumerate(query):
            item.rank = i+1
            item.save()
            
        return True
    
    def player_ranking(self, game):
        """Returns a queryset of the game's players in order of their total scores and player name
        
        :param: The game we want information about
        :type game: object
        :returns: queryset - A list of ScoreCard objects in order of their total scores
        """
        query = self.filter(game=game).order_by('-total_score', 'player_name')
        
        return query
    
class FrameManager(models.Manager):
    """Provides table-level functionality to the Frame model.    
    """
    
    def make_frames(self, score_card):
        """Auto-creates 10 frame objects related to a given ScoreCard
        
        :param score_card: The Score Card each new frame will relate to
        :type score_card: object
        :returns: True
        """
        i = 1
        while i <= 10:
            """foo"""
            params = {'score_card':score_card,
                      'number':i,}
            
            self.create(**params)
            i += 1
            
        return True
    
    def calculate_frames(self, active_frame):
        """Runs through all frames related to a particular score card, and calculates the score for 
        each frame.
        
        :param active_frame: The active frame being bowled
        :type active_frame: object
        :returns: queryset - list of Frame objects for a particular scorecard, ordered according to framenumber
        """
        
        query = self.filter(score_card = active_frame.score_card).order_by('number')
        
        
        # calc total score of the frames to pass to ScoreCard
        ts = 0
        frame_count = len(query)
        for i, frame1 in enumerate(query):
            score = frame1.down_pins1 + frame1.down_pins2
            
            # if on the last frame (10 or 11), break because we don't need to look further ahead
            # This also saves a trip to the db because we arleady tallied the frame's internal score
            # as down_pins1 + down_pins2
            
            # calculate frames 1-10
            if i <= 9:      
            #when only one frame remains                        
                if i == frame_count-2:
                    frame2 = query[i+1]
                    frame3 = None
                    
                # when two or more frames remain
                elif i < frame_count-2:                
                    frame2 = query[i+1]
                    frame3 = query[i+2]
                
                if frame1.is_strike and not frame3:
                    score += frame2.down_pins1 + frame2.down_pins2
                        
                elif frame1.is_strike and frame3:
                    if frame2.is_strike:
                        score += frame2.down_pins1 + frame3.down_pins1
                    else:
                        score += frame2.down_pins1 + frame2.down_pins2
                    
                elif frame1.is_spare:
                    score += frame2.down_pins1
            
            # The values of bonus frames are added to frame 10 -> Bonus frames don't add one-another.
            # for example, if a strike is made on frame 11, it does not get to add the value of frame 12.        
            if i > 9:
                break
                
            frame1.score = score
            frame1.save()
            ts += score
        # instead of using signal, just going to manually call ScoreCard's method 
        # to update its score. can get to scorecard through any of frames in the queryset,
        # so the index used below is arbitrary
        sc = query[0].score_card
        sc.total_score = ts
        sc.save()
        
        return query
    
    
    def frame_count(self, active_card):
        """Counts number of frames related to a particular scorecard. 
        
        :param active_card: The active scorecard being bowled
        :type active_card: object
        :returns: int - count of frames related to active_card
        """
        
        query = self.filter(score_card = active_card).count()
    
        return query
    
    def next_player_and_frame(self, request, player_count, active_card):
        """This function determines which scorecard and frame objects are the next to 
        be active. Save these values to the session.
        
        :param request: the htt prequest object
        :request type: http request object
        :player_count: the number of players (scorecards) in the game
        :type player_count: int
        :param active_card: the active scorecard being bowled
        :type active_card: object
        :returns: object -- returns the session object
        """
        frame_count = self.frame_count(active_card)
        # last frame is false until proven otherwise
        last_frame=False
        
        # re-instantiating player_num and frame_num in the manager (even though it could be passed from the view)
        # I favor decoupling functionality over DRY 
        player_num = int(request.session['player_num'])
        frame_num = int(request.session['frame_num'])

        ############################################################################# 
        #handle a variety of cases depnding on what frame it is and who's turn it is..        
        
        # it's not the last player's turn
        # incraese the player number but not the frame number 
        if player_num < player_count:
            player_num += 1        
            
        # it's the last player's turn, but not the final frame.
        # return to player 1, and increase frame num by 1
        elif player_num == player_count and frame_num < frame_count:
            player_num = 1 
            frame_num += 1
        
        # it's  the last player of the his/her last frame. so the game is over
        elif player_num == player_count and frame_num == frame_count:
            last_frame = True
        
        request.session['player_num'] = player_num
        request.session['frame_num'] = frame_num
        request.session['last_frame'] = last_frame
            
        return request.session    
    
    def create_bonus_frame(self, request, active_frame, active_card):
        """creates a bonus frame, where frame_num > 10.
        
        :param request: the http request object
        :type requset: object
        :param active_frame: the current frame being bowled
        :type active_frame: object
        :param active_card: the current card being bowled
        :type active_card: object
        :returns: object - the newly created bonus frame
        """
        frame_num = request.session['frame_num']
                        
        bonus = self.create(score_card = active_card, number=frame_num +1).save()
        
        return bonus