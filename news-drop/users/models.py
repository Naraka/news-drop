from django.db import models
from django.contrib.auth.models import User


class ImageUser(models.Model):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)