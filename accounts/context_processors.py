from .models import UserProfile
from django.contrib.auth.models import User

def profile(request):
    
    try:
        profile = UserProfile.objects.get(user=request.user)
    except TypeError:
        profile = None
        
    return {'PROFILE':profile}