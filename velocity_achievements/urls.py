from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'velocity_achievements.views.home', name='home'),
    # url(r'^velocity_achievements/', include('velocity_achievements.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', serve, kwargs={'document_root': settings.MEDIA_ROOT}))
