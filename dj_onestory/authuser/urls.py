__author__ = 'Mark'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^loginapi/$', views.login_api, name='loginapi'),
    url(r'^logoutapi/$', views.logout_api, name='logoutapi'),
    url(r'^getuserapi/$', views.get_login_user, name='getuser'),
]