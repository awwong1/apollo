from django.conf.urls import patterns, include, url
from django.contrib import admin
from apollo import views
from apollo.router import router

admin.autodiscover()
urlpatterns = patterns(
    '',
    url(r'^$', views.base, name='base'),
    url(r'^idea/$', views.base_idea, name='base_idea'),
    url(r'^prototype/$', views.base_prototype, name='base_prototype'),
    url(r'^contact/$', views.base_contact, name='base_contact'),
    url(r'^api/', include(router.urls), name='api'),
    url(r'^my-activity/$', views.view_self_activity, name='my_activity'),
    # Internal application urls
    url(r'^asset/', include('applications.assets.urls'), name='assets'),
    url(r'^business/', include('applications.business.urls'), name='business'),
    url(r'^chargelist/', include('applications.charge_list.urls'), name='chargelist'),
    url(r'^pricelist/', include('applications.price_list.urls'), name='pricelist'),
    url(r'^station/', include('applications.station.urls'), name='station'),
    url(r'^termsofservice/', include('applications.terms_of_service.urls'), name='termsofservice'),
    # Included with external packages
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/toggle_staff/', views.toggle_staff_view, name='toggle_staff'),
    url(r'^activity/', include('actstream.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ws_demo/', views.ws_demo, name='ws_demo'),
)