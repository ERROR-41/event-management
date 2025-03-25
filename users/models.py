from django.db import models
from django.contrib.auth.models import AbstractUser
# from cloudinary.models import CloudinaryField
from django import forms


class CustomUser(AbstractUser):
    phone = models.CharField(
        max_length=12, null=True, blank=True, help_text="Enter Phone Number (Optional)" ,default="null"
    )
    profile_picture = models.ImageField(upload_to='upload/profile',null=True,blank=True)
    # profile_picture = CloudinaryField("profile", null=True, blank=True)
    bio = models.TextField(blank=True)

    def get_help_text(self):
        return {
            "phone": self._meta.get_field("phone").help_text,
            "profile_picture": "Upload a profile picture",
            "bio": "Write a short bio about yourself"
        }

    def __str__(self):
        return self.username
