from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from ..models import ScoreCard

class TestCaseHelper(TestCase):
    """Contains commmon functionality for testing the bowling application.
    Please note, this module does not contain any tests itself.
    """ 
    fixtures = ['accounts_views_testdata.json',
                'auth_views_testdata.json',
                'scorecard_views_testdata.json',
                'userena_views_testdata.json',]
    
    username = '0ef86'
    identification = 'sccrespo@gmail.com'
    password = 'a'
    
    game_board_path = reverse('gameboard', kwargs={'username':username})
    
    def signin(self):
        """Sign in the user"""
        response = self.client.post(reverse('userena_signin'),
            {'identification': self.identification,'password': self.password})
    
        return response
    
    def newgame(self):
        """Create new game"""
        self.client.get(reverse('newgame'))
        
    def add_players(self, players=None):
        """Adds a list of players to a game
        :param players: the names of players to be added
        :players type: list
        :returns: response object for final POST request"""
        path = reverse('addplayers', kwargs={'username':self.username})
        
        if players is None:
            players = ['Socrates']
        
        for player in players:                
            response = self.client.post(path, data= {'player_name':player})
        
        return response
    
class ViewsTestCase(TestCaseHelper):
    
    def test_signin(self):
    
        response = self.signin()
        
        self.assertRedirects(response, reverse('userena_profile_detail',
                                               kwargs={'username': self.username}))        
        
    def test_new_game(self):
        
        self.signin()
        
        response = self.client.get(reverse('newgame'))
        
        self.assertEqual(response.status_code, 200)
        
    def test_add_players(self):
        """Tests GET and POST requests for the add_players view"""        
        self.signin()                
        path = reverse('addplayers', kwargs={'username':self.username})        
        # Get and Post Requests
        response_get = self.client.get(path)        
        response_post = self.add_players(['Socrates', 'Carl Marx'])
        # GET Assertions
        self.assertEqual(response_get.status_code, 200)                
        # POST Assertions
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, path)
    
    def test_game_board(self):
        """Tests GET and POST requests for the game_board view"""
        
        self.signin()
        path = self.game_board_path
        # Get and Post Requests
        response_get = self.client.get(path)
        response_post = self.client.post(path, data={'down_pins1':'10',
                                                     'down_pins2':'0'})
        # GET Assertions
        self.assertEqual(response_get.status_code, 200)
        # POST Assertions
        self.assertEqual(response_post.status_code,302)
        self.assertRedirects(response_post, path)
        # Check on Session Data
        self.assertEqual(self.client.session['player_num'], 1)
        self.assertEqual(self.client.session['frame_num'], 2)
        
    def test_game_stats(self):
        """Tests GET requests for the game_stats view"""
        self.signin()
        path = reverse("gamestats")
        
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        
class GameTestCase(TestCaseHelper):

    def test_perfect_game(self):
        """Bowl a Perfect Game and Check for score == 300"""
        self.signin()
        self.newgame()
        self.add_players()
        
        # Bowl 12 frames (instead of 10) because there will be bonus frames
        # created to account for consecutive strikes
        i=0
        while i < 12: 
            self.client.post(self.game_board_path, data={'down_pins1':'10',
                                                         'down_pins2':'0',})
            i+=1
        
        scorecard = ScoreCard.objects.last()
        self.assertEqual(scorecard.total_score, 300)
        
    def test_spare_game(self):
        """Bowl a game of straight Spares and check that score == 100"""
        self.signin()
        self.newgame()
        self.add_players()
        
        i=0
        while i < 11: 
            self.client.post(self.game_board_path, data={'down_pins1':'0',
                                                         'down_pins2':'10',})
            i+=1
            
        scorecard = ScoreCard.objects.last()
        self.assertEqual(scorecard.total_score, 100)