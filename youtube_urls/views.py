import re

from django.contrib import messages
from django.http import HttpResponseRedirect
from urllib.parse import urlparse, parse_qs
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Url

def index(request):
  urls = Url.objects.all()
  return render(request, "youtube_urls/index.html", {"urls": urls})

def detail(request, id):
  url = get_object_or_404(Url, pk = id)
  return render(request, "youtube_urls/detail.html", {"url": url})

def create(request):
  return save(request, "index")

def update(request, id):
  return save(request, "detail", id)

def save(request, view_name, id = None):
  redirect_url = reverse(f"youtube_urls:{view_name}") if id is None else reverse(f"youtube_urls:{view_name}", kwargs = {"id": id})

  try:
    new_url = request.POST["url"]

    if not new_url:
      raise KeyError
  except KeyError:
    messages.error(request, "No URL provided.")
    return HttpResponseRedirect(redirect_url)
  
  # This app supports two YouTube URL formats:
  # https://youtu.be/<Video ID>
  # https://www.youtube.com/watch?v=<Video ID>
  
  # Regular expression for both formats
  pattern = re.compile(
    r"^(https:\/\/)(www\.)?(youtu\.be\/[A-Za-z0-9_-]{11}|youtube\.com\/watch\?v=[A-Za-z0-9_-]{11})$"
  )
  if pattern.match(new_url) is None:
    messages.error(request, "Invalid URL format.")
    return HttpResponseRedirect(redirect_url)
  
  parsed_url = urlparse(new_url)
  query_params = parse_qs(parsed_url.query)
  
  video_id = query_params["v"][0] if "v" in query_params else parsed_url.path.lstrip("/")

  if id is not None:
    url = get_object_or_404(Url, pk = id)
    url.url = new_url
    url.video_id = video_id
  else:
    url = Url(url = new_url, video_id = video_id)
  
  url.save()
  return HttpResponseRedirect(redirect_url)

def delete(_, id):
  url = get_object_or_404(Url, pk = id)
  url.delete()
  return HttpResponseRedirect(reverse("youtube_urls:index"))
