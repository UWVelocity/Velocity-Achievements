from django.conf.urls.defaults import patterns, include, url
from views import achievements

urlpatterns = patterns('',
    url(r'^$', achievements, name='achievements'),
)
