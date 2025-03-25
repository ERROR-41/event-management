from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from django import forms


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=12,default='null',null=True)
    profile_picture = CloudinaryField("profile", null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self):
        return self.username
    
    
