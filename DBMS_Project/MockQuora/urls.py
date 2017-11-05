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
                       url(r'^answer/(?P<question_id>\d+)/(?P<answer_id>\d+)/$', views.answer_page, name='answer_page'),
                       url(r'^follow/(?P<follow_id>\d+)/(?P<followed_id>\d+)/$', views.follow, name='follow'),
                       url(r'^follow_profile/(?P<followed_id>\d+)/$', views.follow_profile, name='follow_profile'),
                       url(r'^vote/(?P<vote_id>\d+)/(?P<answer_id>\d+)/(?P<comment_id>\d+)/(?P<flag>\d+)/$',
                           views.votes, name='votes'),
                       url(r'^profile/(?P<user_id>\d+)/$', views.profile, name='profile'),
                       url(r'^message/(?P<user_id>\d+)/$', views.message, name='message'),
                       url(r'^bookmark/(?P<answer_id>\d+)/$', views.bookmark, name='bookmark'),
                       url(r'^chat/$', views.chat, name='chat'),
                       url(r'^notifications/$', views.notifications, name='notifications'),
                       url(r'^logout/$', views.user_logout, name='logout'),
                       url(r'^askto/(?P<question_id>\d+)/$', views.askto, name='askto'),
                       )
