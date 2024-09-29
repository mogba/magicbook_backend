from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from urllib.parse import urlparse, parse_qs

from .models import Url

def index(request):
  urls = Url.objects.all()
  return render(request, "youtube_urls/index.html", {"urls": urls})

def detail(request, id):
  url = get_object_or_404(Url, pk = id)
  return render(request, "youtube_urls/detail.html", {"url": url})

def save(request, id = None):
  try:
    new_url = request.POST["url"]
  except KeyError:
    return render(request, "youtube_urls/index.html", {"error_message": "No URL provided."})
  
  parsed_url = urlparse(new_url)
  query_params = parse_qs(parsed_url.query)

  # This addresses the following cases:
  # https://youtu.be/<video_id>
  # https://www.youtube.com/watch?v=<video_id>
  video_id = query_params["v"][0] if "v" in query_params else parsed_url.path.lstrip("/")
  
  if (id is not None):
    url = get_object_or_404(Url, pk = id)
    url.url = new_url
    url.video_id = video_id
  else:
    url = Url(url = new_url, video_id = video_id)
  
  url.save()
  return HttpResponseRedirect(reverse("youtube_urls:index"))

def delete(_, id):
  url = get_object_or_404(Url, pk = id)
  url.delete()
  return HttpResponseRedirect(reverse("youtube_urls:index"))
