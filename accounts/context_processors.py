from .models import UserProfile
from django.contrib.auth.models import User

def accounts_context(request):
    
    if request.user.is_authenticated():
        profile = UserProfile.objects.get(user=request.user)
    else:
        profile = None
        
    return {'PROFILE':profile}