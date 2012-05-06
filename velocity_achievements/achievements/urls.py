from django.conf.urls.defaults import patterns, include, url
from views import achievements, nominate, nominations_list
from models import Participant
from emailauth.views import signup

urlpatterns = patterns('',
    url(r'^$', achievements, name='achievements'),
    url(r'^nominate/(?P<participant_id>.+)/$', nominate, name='nominate'),
    url(r'^signup/$', signup, name='signup', kwargs={'user_class': Participant}),
    url(r'^nominations/$', nominations_list, name='nominate'),
)
