from rest_framework import serializers
from songs.serializers import SongSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Song
from .serializers import SongSerializer


class SongListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        songs = Song.objects.all()
        serialized_songs = SongSerializer(songs, many=True)
        return Response(serialized_songs.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner'] = request.user.id
        new_song = SongSerializer(data=request.data)
        if new_song.is_valid():
            new_song.save()
            return Response(new_song.data, status=status.HTTP_201_CREATED)
        return Response(new_song.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


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

    