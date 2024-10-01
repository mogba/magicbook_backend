from django.contrib.auth.models import User
from django.db import models

class Url(models.Model):
    url = models.CharField("URL", max_length = 100)
    video_id = models.CharField("Video ID", max_length = 32)
    date_updated = models.DateTimeField("Date updated", auto_now = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)

    def __str__(self):
      return self.url
