from django.conf.urls import patterns, url
from apps.price_list import views

urlpatterns = patterns(
    '',
    # Price List
    url(r'^$', views.PriceListViewList.as_view(), name='pricelist_list'),
    url(r'^create/$', views.PriceListViewCreate.as_view(), name='pricelist_create'),
    url(r'^(?P<pl_id>\d)/$', views.PriceListViewDetail.as_view(), name='pricelist_detail'),
    url(r'^(?P<pl_id>\d)/update/$', views.PriceListViewUpdate.as_view(), name='pricelist_update'),
    url(r'^(?P<pl_id>\d)/delete/$', views.PriceListViewDelete.as_view(), name='pricelist_delete'),
    # Equipment Relation
    url(r'^(?P<pl_id>\d)/create/equipment/(?P<item_uuid>.*)/$', views.PriceListItemEquipmentViewCreate.as_view(),
        name='equipment_pricelistitem_create'),
    url('equipment_relation/(?P<pk>\d)/$', views.PriceListItemEquipmentViewDetail.as_view(),
        name='equipment_pricelistitem_detail'),
    url('equipment_relation/(?P<pk>\d)/update/$', views.PriceListItemEquipmentViewUpdate.as_view(),
        name='equipment_pricelistitem_update'),
    url('equipment_relation/(?P<pk>\d)/delete/$', views.PriceListItemEquipmentViewDelete.as_view(),
        name='equipment_pricelistitem_delete'),
    # Activity Item
    url(r'^(?P<pl_id>\d)/create/activity/$', views.ActivityPriceListItemViewCreate.as_view(),
        name='activity_pricelistitem_create'),
    url(r'^activity/(?P<pk>\d)/$', views.ActivityPriceListItemViewDetail.as_view(),
        name='activity_pricelistitem_detail'),
    url(r'^activity/(?P<pk>\d)/update/$', views.ActivityPriceListItemViewUpdate.as_view(),
        name='activity_pricelistitem_update'),
    url(r'^activity/(?P<pk>\d)/delete/$', views.ActivityPriceListItemViewDelete.as_view(),
        name='activity_pricelistitem_delete'),
    # Time Item
    # Unit Item
)