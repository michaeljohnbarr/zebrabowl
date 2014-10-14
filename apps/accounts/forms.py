from django import forms
from django.contrib.auth.models import User
import os
import re

class NewUserForm(forms.Form):
	
	first_name = forms.TextInput()
	last_name = forms.TextInput()
	
		
		
