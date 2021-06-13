from songs.models import Song
from django.urls import path
from django.urls import path
from .views import (
    SongListView,
    SongDetailView
    )


urlpatterns = [
    path('', SongListView.as_view()),
    path('<int:pk>/', SongDetailView.as_view()),
]