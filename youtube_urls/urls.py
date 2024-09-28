from django.urls import path

from . import views

app_name = "youtube_urls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>/", views.detail, name="detail"),
    path("save/", views.save, name="create"),
    path("save/<int:id>/", views.save, name="update"),
    path("delete/<int:id>/", views.delete, name="delete"),
]