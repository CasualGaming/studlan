from django.conf.urls.defaults import *

urlpatterns = patterns('studlan.userprofile.views',
    url(r'^$', 'my_profile', name='myprofile'),
    url(r'^update/$', 'update_profile', name='update_profile'),
    url(r'^history/$', 'history', name='user_history'),
    url(r'^(?P<username>[\w-]+)/$', 'user_profile', name='profile'),
)
