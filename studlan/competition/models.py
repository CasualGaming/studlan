from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    nick = models.CharField('nick', max_length=20,
                            help_text='Specify a nick name (display name).')

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
