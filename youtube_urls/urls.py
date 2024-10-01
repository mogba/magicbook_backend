from django.urls import path

from .views import YouTubeUrlsListApiView, YouTubeUrlsDetailApiView

app_name = "youtube_urls"

urlpatterns = [
    path("", YouTubeUrlsListApiView.as_view()),
    path("<int:id>/", YouTubeUrlsDetailApiView.as_view()),
]