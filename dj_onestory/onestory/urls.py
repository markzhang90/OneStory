__author__ = 'Mark'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.userview.login, name='login'),
    url(r'^feed/$', views.allviews.feed, name='feed'),
    url(r'^logintosys/$', views.allviews.login_to_sys, name='loginpost'),
    url(r'^register/$', views.register_to_onestory, name='register'),
    url(r'^getaccount/$', views.get_log_in_user, name='get_log_in_user'),
    url(r'^insertarticle/$', views.insert_article, name='insert_article'),
    url(r'^updatearticle/$', views.update_article, name='update_article'),
    url(r'^deletearticle/$', views.del_article, name='del_article'),
    url(r'^updatearticlestatus/$', views.update_article_status, name='update_article_status'),
    url(r'^getarticle/$', views.get_article_by_id, name='get_article_by_id'),
    url(r'^getuserarticles/$', views.get_article_list_by_uid, name='get_article_list_by_uid'),
]
