from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Song, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_image')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class PopulatedCommentSerializer(CommentSerializer):
    owner = UserSerializer()


class PopulatedSongSerializer(SongSerializer):
    comments = PopulatedCommentSerializer(many=True)
    liked_by = UserSerializer(many=True)
    owner = UserSerializer()