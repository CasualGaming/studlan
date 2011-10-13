import datetime

from django.db import models

class Article(models.Model):
    title = models.CharField("title", max_length=50)
    body = models.TextField("body")
    published_datetime = models.DateTimeField("published", default=datetime.datetime.now)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-published_datetime']
