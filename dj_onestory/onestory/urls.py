__author__ = 'Mark'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logintosys/$', views.login_to_sys, name='loginpost'),
    url(r'^logintosys2/$', views.login_to_sys2, name='loginpost2'),
]