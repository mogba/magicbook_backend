from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

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

  if (id is not None):
    url = get_object_or_404(Url, pk = id)
    url.url = new_url
  else:
    url = Url(url = new_url)
  
  url.save()
  return HttpResponseRedirect(reverse("youtube_urls:index"))

def delete(_, id):
  url = get_object_or_404(Url, pk = id)
  url.delete()
  return HttpResponseRedirect(reverse("youtube_urls:index"))
