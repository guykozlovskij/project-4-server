from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.json import JSONField

class User(AbstractUser):
    email = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=250, default='https://thumbs.dreamstime.com/b/default-avatar-profile-icon-vector-social-media-user-portrait-176256935.jpg')
    #! bio = models.CharField(max_length=400)
    #! liked_songs = JSONField()
