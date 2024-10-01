from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Core
    path("api/admin/", admin.site.urls),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # Apps
    path("api/youtube-urls/", include("youtube_urls.urls"), name = "youtube_urls"),
]
