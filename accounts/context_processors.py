from .models import UserProfile
from django.contrib.auth.models import User

def profile(request):
    
    profile = UserProfile.objects.get(user=request.user)
    
        
    return {'PROFILE':profile}