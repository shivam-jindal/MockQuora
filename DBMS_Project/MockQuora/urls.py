from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^login/$', views.user_login, name='login'),
                       url(r'^add_details/$', views.add_profile_details, name='add_details'),
                       url(r'^register/$', views.register_user, name='register'),
                       url(r'^feed/$', views.feed, name='feed'),
                       url(r'^post_question/$', views.post_question, name='post_question'),
                       url(r'^question/(?P<question_id>\d+)/$', views.question_page, name='question_page'),
                       url(r'^follow/(?P<follow_id>\d+)/(?P<followed_id>\d+)/$', views.follow, name='follow'),
                       url(r'^profile/(?P<user_id>\d+)/$', views.profile, name='profile'),
                       url(r'^message/(?P<user_id>\d+)/$', views.message, name='message'),
                       url(r'^chat/$', views.chat, name='chat'),
                       )
