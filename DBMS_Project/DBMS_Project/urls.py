from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DBMS_Project.views.home', name='home'),
    url(r'^quora/', include('MockQuora.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
