from accounts.models import UserProfile
from django.core.management.base import NoArgsCommand
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class Command(NoArgsCommand):
    help = 'Changes site name to appropriate URL'
    
    def handle_noargs(self,**options):            
        
        ############## Site Setup ####################
        # change site to the appropriate URL        
        
        site_params = {"domain":"localhost:8000",
                       "name":"zebrabowl",
                       }
        
        Site.objects.filter(pk=1).update(**site_params)
        
        self.stdout.write("done.")