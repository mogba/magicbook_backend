import re

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from urllib.parse import urlparse, parse_qs

from core.serializers import ModelSerializer
from infra.permissions import IsOwner

from .models import Url

class CustomApiView(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated, IsOwner, permissions.IsAuthenticated]


class YouTubeUrlsListApiView(CustomApiView):
  def get(self, request):
    """
    Lists all URLs for the current user.
    """
    urls = Url.objects.filter(user = request.user.id)

    if urls.count() == 0:
      return Response({ "error": "No URLs found" }, status = status.HTTP_404_NOT_FOUND)

    serializer = ModelSerializer(urls, many = True)
    return Response(serializer.data, status = status.HTTP_200_OK)

  def post(self, request):
    """
    Creates a new URL for the current user.
    """
    return save(request)


class YouTubeUrlsDetailApiView(CustomApiView):
  def get(self, request, id):
    """
    Lists a URL by a given ID.
    """
    url = get_object(id, request.user)

    if not url:
      return Response(data = { "error": "URL not found." }, status = status.HTTP_404_NOT_FOUND)

    serializer = ModelSerializer(url, many = False)
    return Response(serializer.data, status = status.HTTP_200_OK)
  
  def put(self, request, id):
    """
    Updates a URL by a given ID.
    """
    return save(request, id)
  
  def delete(self, request, id):
    """
    Deletes a URL by a given ID.
    """
    url = get_object(id, request.user)
    if not url:
      return Response(data = { "error": "URL not found." }, status = status.HTTP_404_NOT_FOUND)

    url.delete()
    return Response(status = status.HTTP_200_OK)
  

def get_object(id, user):
  """
  Gets an object by a given ID. If the object does not exist, returns None.
  """
  try:
    return Url.objects.get(id = id, user = user)
  except Url.DoesNotExist:
    return None

def save(request, id = None):
  """
  Creates or updates a URL. Updates require an ID.
  """
  url = request.data.get("url")

  if not url:
    return Response(data = { "error": "No URL provided." }, status = status.HTTP_400_BAD_REQUEST)
  
  # This app supports two YouTube URL formats:
  # https://youtu.be/<Video ID>
  # https://www.youtube.com/watch?v=<Video ID>
  
  # Regular expression for both formats
  # A URL like the following is invalid: https://www.youtube.com/watch?v=-VCJEEOroZM&t=31s. Need to address that.
  pattern = re.compile(
    r"^(https:\/\/)(www\.)?(youtu\.be\/[A-Za-z0-9_-]{11}|youtube\.com\/watch\?v=[A-Za-z0-9_-]{11})$"
  )
  if not pattern.match(url):
    return Response(data = { "error": "Unsupported URL format." }, status = status.HTTP_400_BAD_REQUEST)
  
  parsed_url = urlparse(url)
  query_params = parse_qs(parsed_url.query)
  
  video_id = query_params["v"][0] if "v" in query_params else parsed_url.path.lstrip("/")

  if id is not None:
    url_object = get_object(id, request.user)

    if not url_object:
      return Response(data = { "error": "URL not found." }, status = status.HTTP_404_NO_CONTENT)

    url_object.url = url
    url_object.video_id = video_id
  else:
    url_object = Url(url = url, video_id = video_id, user = request.user)
  
  url_object.save()
  return Response(status = status.HTTP_200_OK)
