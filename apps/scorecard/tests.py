from django.test import TestCase
from .models import *

class GameTestCase(TestCase):
    def set_up(self):
        Game.objects.create(game_hash="myfakehash")
