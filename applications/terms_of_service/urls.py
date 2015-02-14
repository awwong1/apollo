from django.conf.urls import patterns, url
from applications.terms_of_service import views

urlpatterns = patterns(
    '',
    url(r'^$', views.TermsOfServiceViewList.as_view(), name='termsofservice_list'),
    url(r'^create/$', views.TermsOfServiceViewCreate.as_view(), name='termsofservice_create'),
    url(r'^(?P<pk>\d)/$', views.TermsOfServiceViewDetail.as_view(), name='termsofservice_detail'),
    url(r'^(?P<pk>\d)/update/$', views.TermsOfServiceViewUpdate.as_view(), name='termsofservice_update'),
    url(r'^(?P<pk>\d)/delete/$', views.TermsOfServiceViewDelete.as_view(), name='termsofservice_delete'),
)