from songs.models import Song
from django.urls import path
from django.urls import path
from .views import (
    SongListView,
    SongDetailView,
    CommentListView,
    CommentDetailView
    )


urlpatterns = [
    path('', SongListView.as_view()),
    path('<int:pk>/', SongDetailView.as_view()),
    path('<int:song_pk>/comments/', CommentListView.as_view()),
    path('<int:_>/comments/<int:comment_pk>/', CommentDetailView.as_view()),
]