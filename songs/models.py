from django.contrib.admin.sites import NotRegistered
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=20)
    # ! Might need to be changed
    notes = models.JSONField()
    likes = models.PositiveBigIntegerField()
    tempo =  models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(180)]
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='created_songs',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name}'


#! Notes model