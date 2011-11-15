from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models

class Activity(models.Model):
	title = models.CharField('title', max_length=50)
	image_url = models.CharField('image_url', max_length=100, blank=True)
	desc = models.TextField('description')

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = 'activity'
		verbose_name_plural = 'activities'

class Competition(models.Model):
	STATUS_OPTIONS = (
		(1, 'Open'),
		(2, 'Closed'),
		(3, 'In progress'),
		(4, 'Finished')
	)
	title = models.CharField('title', max_length=50)
	status = models.SmallIntegerField("status", choices=STATUS_OPTIONS)
	activity = models.ForeignKey(Activity)
	participants = models.ManyToManyField(User)
	desc = models.TextField('description')

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['status']

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    nick = models.CharField('nick', max_length=20,
                            help_text='Specify a nick name (display name).')

    def __unicode__(self):
    	return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User, dispatch_uid="users-profilecreation-signal")
