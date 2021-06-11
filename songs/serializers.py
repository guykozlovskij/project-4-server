from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Song
User = get_user_model()

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'