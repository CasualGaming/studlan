from django.conf.urls.defaults import *

urlpatterns = patterns('studlan.userprofile.views',
    url(r'^$', 'my_profile', name='myprofile'),
    url(r'^(?P<username>\w+)$', 'user_profile', name='profile'),
)
