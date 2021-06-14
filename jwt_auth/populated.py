from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from songs.serializers import CommentSerializer, SongSerializer

User = get_user_model()

class PopulatedUserSerializer(ModelSerializer):
    liked_songs = SongSerializer(many=True)
    comments = CommentSerializer(many=True)
    created_songs = SongSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'liked_songs',
            'profile_image',
            'email',
            'comments',
            'created_songs'
        )
