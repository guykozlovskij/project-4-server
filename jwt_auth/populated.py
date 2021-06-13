from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from songs.serializers import SongSerializer
#! from dinosaurs.serializers import CommentSerializer

User = get_user_model()

class PopulatedUserSerializer(ModelSerializer):
    #! favorites = SongSerializer(many=True)
    #! comments = CommentSerializer(many=True)
    created_songs = SongSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            # 'profile_image',
            'email',
            # 'favorites',
            # 'comments',
            'created_songs'
        )
