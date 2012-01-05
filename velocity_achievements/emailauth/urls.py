from django.conf.urls.defaults import *
import forms
import views
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
    url(r'^login/$', auth_views.login, name="customerlogin", kwargs={'authentication_form': forms.AuthenticationForm}),
    url(r'^logout/$', auth_views.logout_then_login, name="customerlogout", kwargs={'login_url': 'customerlogin'}),
    url(r'^activate/(?P<token>[0-9A-Za-z]{40})/', views.initial_password_set, name='activate'),
    url(r'^password_change/$', auth_views.password_change, name = 'change_password', kwargs={"post_change_redirect": 'useraccount'}),
#    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
#    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
#    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm'),
#    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^dispatch/$', views.dispatch, name="dispatch")
)
