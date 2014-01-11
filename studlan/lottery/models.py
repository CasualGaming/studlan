from django.db import models
from django.contrib.auth.models import User
from translatable.models import TranslatableModel, get_translation_model

class Lottery(TranslatableModel):
    lan = models.ForeignKey(LAN)
    registration_open = models.BooleanField('Open', default=False)


class LotteryTranslation(get_translation_model(Lottery, 'lottery'):
    title = models.CharField('title', max_length=50)
    description = models.TextField('description')

    def __unicode__(self):
        return self.title


class Participant(models.Model):
    lottery = models.ForeignKey(Lottery)
    user = models.ForeignKey(User)

class Winner(models.Model):
    lottery = models.ForeignKey(Lottery)
    user = models.ForeignKey(User)
