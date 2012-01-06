from django.conf.urls.defaults import patterns, include, url
from views import achievements
from models import Participant
from emailauth.views import signup

urlpatterns = patterns('',
    url(r'^$', achievements, name='achievements'),
    url(r'^signup/$', signup, name='signup', kwargs={'user_class': Participant})
)
