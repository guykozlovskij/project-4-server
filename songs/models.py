from django.contrib.admin.sites import NotRegistered
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Song(models.Model):
    name = models.CharField(max_length=20)
    notes = models.JSONField()
    liked_by = models.ManyToManyField(
        'jwt_auth.User',
        related_name='liked_songs',
        blank=True
    )
    tempo = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(180)]
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='created_songs',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name}'


class Comment(models.Model):
    content = models.TextField(max_length=250)
    song = models.ForeignKey(
        Song,
        related_name='comments',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'jwt_auth.User',
        related_name='comments',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'Comment {self.id} on {self.song}'

#! Notes model
