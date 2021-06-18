from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields.json import JSONField

class User(AbstractUser):
    email = models.CharField(max_length=50)
    profile_image = models.CharField(max_length=250)
    #! bio = models.CharField(max_length=400)
    #! liked_songs = JSONField()
