from django.conf.urls import patterns, include, url
from django.contrib import admin
from apollo.views import index, ws_demo

admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^$', index, name='index'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ws_demo/', ws_demo, name='ws_demo'),
)