from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django_countries.fields import CountryField
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    photo = CloudinaryField('profile_pics/', blank=True)

    def save_profile(self):
        self.save()                   

    def delete_profile(self):
        self.delete()
    
    def __str__(self):
        return self.bio
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'  
