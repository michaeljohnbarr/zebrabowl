def session_required(_view):
    def _wrap(request, *args, **kwargs):
        # try to get vars from Django session. If they don't exist (KeyError), then the game just started
        # and we need to create intial session values. 
        try:        
            request.session['player_num'] 
            request.session['frame_num']
        except KeyError:
            request.session['player_num'] = 1
            request.session['frame_num'] = 1
        
        return _view(request,*args,**kwargs)
    return _wrap


def flush_session(_view):
    """Ensures session is wiped out for starting new games"""
    
    def _wrap(request, *args, **kwargs):
        request.session.flush()
        
        return _view(request, *args, **kwargs)
    return _wrap