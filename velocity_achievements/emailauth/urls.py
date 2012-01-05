from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import forms
import views
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^login/$', auth_views.login, name="login", kwargs={'authentication_form': forms.AuthenticationForm, 'template_name': 'emailauth/login.html'}),
    url(r'^logout/$', auth_views.logout_then_login, name="logout", kwargs={'login_url': '/login'}),
    url(r'^activate/(?P<token>[0-9A-Za-z]{40})/', views.initial_password_set, name='activate'),
    url(r'^password_change/$', auth_views.password_change, name = 'change_password', kwargs={"post_change_redirect": 'achievements'}),
    url(r'^signed_up/$', direct_to_template, name='will_notify', kwargs={'template': 'emailauth/will_notify.html'}),
)
