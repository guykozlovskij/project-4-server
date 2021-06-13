from rest_framework import serializers
from songs.serializers import SongSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied

from .models import Song
from .serializers import SongSerializer


class SongListView(APIView):

    def get(self, _request):
        songs = Song.objects.all()
        serialized_songs = SongSerializer(songs, many=True)
        return Response(serialized_songs.data, status=status.HTTP_200_OK)


class SongDetailView(APIView):

    def get_song(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise NotFound()

    def get(self, _request, pk):
        song = self.get_song(pk=pk)
        serialized_song = SongSerializer(song)
        return Response(serialized_song.data, status=status.HTTP_200_OK)