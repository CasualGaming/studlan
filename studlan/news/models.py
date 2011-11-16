import datetime

from django.db import models

class Article(models.Model):
    title = models.CharField("title", max_length=50)
    body = models.TextField("body")
    pub_date = models.DateTimeField("published", default=datetime.datetime.now)

    def __unicode__(self):
        return self.title
    
    def count():
    	return count(Article.objects.all())

    class Meta:
        ordering = ['-pub_date']
