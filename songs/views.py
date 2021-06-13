from rest_framework import serializers
from songs.serializers import SongSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Song, Comment
from .serializers import SongSerializer, PopulatedSongSerializer, CommentSerializer


class SongListView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, _request):
        songs = Song.objects.all()
        serialized_songs = PopulatedSongSerializer(songs, many=True)
        return Response(serialized_songs.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['owner'] = request.user.id
        new_song = SongSerializer(data=request.data)
        if new_song.is_valid():
            new_song.save()
            return Response(new_song.data, status=status.HTTP_201_CREATED)
        return Response(new_song.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class SongDetailView(APIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_song(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise NotFound()

    def get(self, _request, pk):
        song = self.get_song(pk=pk)
        serialized_song = PopulatedSongSerializer(song)
        return Response(serialized_song.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        song_to_update = self.get_song(pk=pk)
        if song_to_update.owner != request.user:
            raise PermissionDenied()
        request.data['owner'] = request.user.id
        updated_song = SongSerializer(song_to_update, data=request.data)
        if updated_song.is_valid():
            updated_song.save()
            return Response(updated_song.data, status=status.HTTP_202_ACCEPTED)
        return Response(updated_song.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        song_to_delete = self.get_song(pk=pk)
        if song_to_delete.owner != request.user:
            raise PermissionDenied()
        song_to_delete.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#?-----------------------------------------------------------------


class CommentListView(APIView):

    permission_classes = (IsAuthenticated, )

    def post(self, request, song_pk):
        request.data['song'] = song_pk
        serialized_comment = CommentSerializer(data=request.data)
        if serialized_comment.is_valid():
            serialized_comment.save()
            return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
        return Response(serialized_comment.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CommentDetailView(APIView):

    permission_classes = (IsAuthenticated, )
    
    def delete(self, _request, _, comment_pk):
        try:
            comment_to_delete = Comment.objects.get(pk=comment_pk)
            comment_to_delete.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            raise NotFound()