from django.db import models

class Url(models.Model):
    url = models.CharField("URL", max_length=100)
    date_created = models.DateTimeField("Date created", auto_now_add=True)

    def __str__(self):
      return self.url
