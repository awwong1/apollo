from applications.business import views
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url('^$', views.BusinessViewList.as_view(), name='business_list'),
    url('^create/$', views.BusinessViewCreate.as_view(), name='business_create'),
    url('^(?P<pk>\d*)/$', views.BusinessViewDetail.as_view(), name='business_detail'),
    url('^(?P<pk>\d*)/update/$', views.BusinessViewUpdate.as_view(), name='business_update'),
    url('^(?P<pk>\d*)/delete/$', views.BusinessViewDelete.as_view(), name='business_delete'),
)