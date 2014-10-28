"""
.. module:: decorators.py
    :Synopsis: A module containing custom view decorators.
"""

from .models import Game

def session_required(_view):
    """
    Ensures that the proper session data exists. If if doesn't,
    this decorator will create the initial session data required for the game.
    
    :param _view: the view function to be wrapped
    :type name: function
    :returns: wrapper function        
    """
    
    def _wrap(request, *args, **kwargs):
        # try to get vars from Django session. If they don't exist (KeyError), then the game just started
        # and we need to create intial session values. 
        try:        
            request.session['player_num'] 
            request.session['frame_num']
        except KeyError:
            request.session['player_num'] = 1
            request.session['frame_num'] = 1
            
        try: 
            request.session['game_hash']
        except KeyError:
            game = Game.objects.last()
            request.session['game_hash'] = game.game_hash 
        
        return _view(request,*args,**kwargs)
    return _wrap


def new_game_session(_view):
    """
    Ensures any previous game's session variables
    are re-set to None before starting a new game.
    
    :param _view:the view function to be wrapped
    :type _view: function
    :returns: wrapper function    
    """
    
    def _wrap(request, *args, **kwargs):
        del request.session['player_num']
        del request.session['frame_num']
        del request.session['game_hash']
        
        return _view(request, *args, **kwargs)
    return _wrap