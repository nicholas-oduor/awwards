from django import forms
from .models import *


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Projects
        exclude = ['author', 'pub_date', 'author_profile']
        widgets = {
          'project_description': forms.Textarea(attrs={'rows':4, 'cols':10,}),
        }
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widgets = {
          'bio': forms.Textarea(attrs={'rows':2, 'cols':10,}),
        }