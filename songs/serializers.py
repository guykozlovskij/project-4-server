from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Song, Comment

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class PopulatedSongSerializer(SongSerializer):
    comments = CommentSerializer(many=True)
    # favorited_by = UserSerializer(many=True)
    owner = UserSerializer()