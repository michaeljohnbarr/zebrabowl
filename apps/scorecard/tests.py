from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class ViewsTestCase(TestCase):
    
    fixtures = ['accounts_views_testdata.json',
                'auth_views_testdata.json',
                'scorecard_views_testdata.json',
                'userena_views_testdata.json',]
    
    username = '0ef86'
    identification = 'sccrespo@gmail.com'
    password = 'a'
    
    def signin(self):
        
        response = self.client.post(reverse('userena_signin'),
            {'identification': self.identification,'password': self.password})
    
        return response
    
    def test_signin(self):
    
        response = self.signin()
        
        self.assertRedirects(response, reverse('userena_profile_detail',
                                               kwargs={'username': self.username}))
        
        
    def test_new_game(self):
        
        self.signin()
        
        response = self.client.get(reverse('newgame'))
        
        self.assertEqual(response.status_code, 200)
        
    def test_add_players(self):
        
        
        self.signin()                
        path = (reverse('addplayers', kwargs={'username':self.username}))        
        # Get and Post Requests
        response_get = self.client.get(path)        
        response_post = self.client.post(path, data= {'player_name':'Socrates'})
        # Assertions
        self.assertEqual(response_get.status_code, 200)        
        self.assertEqual(response_post.status_code, 302)
        self.assertRedirects(response_post, path)