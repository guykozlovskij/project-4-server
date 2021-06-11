from rest_framework import serializers
from songs.serializers import SongSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Song
from .serializers import SongSerializer
# Create your views here.

class SongListView(APIView):

    def get(self, request):
        songs = Song.objects.all()
        serialized_songs = SongSerializer(songs, many=True)
        return Response(serialized_songs.data, status=status.HTTP_200_OK)
