from django.conf.urls import patterns, url
from apps.price_list import views

urlpatterns = patterns(
    '',
    url(r'^$', views.PriceList_List.as_view(), name='pricelist_list'),
    url(r'^create/$', views.PriceList_Create.as_view(), name='pricelist_create'),
    url(r'^(?P<pl_id>\d)/$', views.PriceList_Detail.as_view(), name='pricelist_detail'),
    url(r'^(?P<pl_id>\d)/update/$', views.PriceList_Update.as_view(), name='pricelist_update'),
    url(r'^(?P<pl_id>\d)/delete/$', views.PriceList_Delete.as_view(), name='pricelist_delete'),
    # Activity Item Creation
    url(r'^(?P<pl_id>\d)/create/activity/$', views.ActivityPriceListItem_Create.as_view(), name='activitypli_create'),
)