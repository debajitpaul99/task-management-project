from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.db.models.signals import post_delete
from django.dispatch import receiver


class UserProfile(AbstractUser):
    profile_image = models.ImageField(blank=True, upload_to="profile_img", default="profile_img/default_profile_pic.jpg")
    bio = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.profile_image:
            self.profile_image = "profile_img/default_profile_pic.jpg"
        return super().save(*args, **kwargs)
