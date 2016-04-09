__author__ = 'Mark'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logintosys/$', views.login_to_sys, name='loginpost'),
    url(r'^getaccount/$', views.get_log_in_user, name='get_log_in_user'),
]