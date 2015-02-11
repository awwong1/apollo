from django.conf.urls import patterns, url
from apps.price_list import views

urlpatterns = patterns(
    '',
    url(r'^$', views.PriceListViewList.as_view(), name='pricelist_list'),
    url(r'^create/$', views.PriceListViewCreate.as_view(), name='pricelist_create'),
    url(r'^(?P<pl_id>\d)/$', views.PriceListViewDetail.as_view(), name='pricelist_detail'),
    url(r'^(?P<pl_id>\d)/update/$', views.PriceListViewUpdate.as_view(), name='pricelist_update'),
    url(r'^(?P<pl_id>\d)/delete/$', views.PriceListViewDelete.as_view(), name='pricelist_delete'),
    # Activity Item Creation
    url(r'^(?P<pl_id>\d)/create/activity/$', views.ActivityPriceListItemViewCreate.as_view(),
        name='activity_pli_create'),
)