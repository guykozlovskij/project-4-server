from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Song
User = get_user_model()


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class PopulatedSongSerializer(SongSerializer):
    # comments = PopulatedCommentSerializer(many=True)
    # favorited_by = UserSerializer(many=True)
    owner = UserSerializer()
