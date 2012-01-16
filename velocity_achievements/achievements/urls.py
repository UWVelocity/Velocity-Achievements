from django.conf.urls.defaults import patterns, include, url
from views import achievements, nominate, nominate_person
from models import Participant
from emailauth.views import signup

urlpatterns = patterns('',
    url(r'^$', achievements, name='achievements'),
    url(r'^nominate/$', nominate, name='nominate'),
    url(r'^nominate/(?P<participant_id>.+)/$', nominate_person, name='nominate'),
    url(r'^signup/$', signup, name='signup', kwargs={'user_class': Participant})
)
