from django.db import models

#class Competition(models.Model):

class Participant(models.Model):
    nick = models.CharField('nick', max_length=50)
    first_name = models.CharField('first name', max_length=50)
    last_name = models.CharField('last name', max_length=100)
    email = models.CharField('email address', max_length=100)

    def __unicode__(self):
        return self.nick

    class Meta:
        ordering = ['nick']
