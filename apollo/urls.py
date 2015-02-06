from django.conf.urls import patterns, include, url
from django.contrib import admin
from apollo.views import base, base_idea, base_prototype, base_contact, ws_demo
from apollo.router import router

admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^$', base, name='base'),
    url(r'^idea/$', base_idea, name='base_idea'),
    url(r'^prototype/$', base_prototype, name='base_prototype'),
    url(r'^contact/$', base_contact, name='base_contact'),
    url(r'^api/', include(router.urls), name='api'),
    # Included with external packages
    url(r'^accounts/', include('allauth.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ws_demo/', ws_demo, name='ws_demo'),
)