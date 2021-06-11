from django.urls import path
from django.urls import path
from .views import SongListView


urlpatterns = [
    path('', SongListView.as_view())
]