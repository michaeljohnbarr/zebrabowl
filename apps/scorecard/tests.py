from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class ViewsTestCase(TestCase):
    
    client = Client()
    
    def test_signin(self):
    
        response = self.client.post(reverse('userena_signin'),
                                    {'identification': 'sccrespo@gmail.com','password': 'a'})
        
        self.assertRedirects(response, reverse('userena_profile_detail',
                                               kwargs={'username': '0ef86'}))
        
        
    def test_new_game(self):
        
        response = self.client.get(reverse('newgame'))
        
        self.assertEqual(response.status_code, 200)