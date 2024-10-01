from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # Swagger 
    path('api/schema/', SpectacularAPIView.as_view(), name = 'schema'),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name = "schema"), name = "swagger-ui"),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name = "schema"), name = "redoc"),
    # Core
    path("api/admin/", admin.site.urls),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # Apps
    path("api/youtube-urls/", include("youtube_urls.urls"), name = "youtube_urls"),
]
