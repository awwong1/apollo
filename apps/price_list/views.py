from apollo.choices import PRICE_LIST_PRE_RELEASE
from apollo.viewmixins import LoginRequiredMixin
from apps.price_list.forms import ActivityPriceListItemForm, PriceListForm, PriceListItemEquipmentForm, \
    PriceListItemServiceForm
from apps.price_list.models import PriceList, ActivityPriceListItem, PriceListItemEquipment, PriceListItemService
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def PriceListItemRedirect(request, pl_id=None, item_uuid=None):
    """
    Given a price list item id and an item guid, redirect to the price list item detail page.
    """
    price_list = get_object_or_404(PriceList, pk=pl_id)
    act_items = ActivityPriceListItem.objects.filter(price_list=price_list, item_uuid=item_uuid)
    if len(act_items) > 0:
        return redirect('activity_pricelistitem_detail', pk=act_items[0].pk)
    raise Http404(
        "No item exists with price list id {pl_id} and item uuid {item_uuid}".format(pl_id=pl_id, item_uuid=item_uuid)
    )


"""
Price list model generic views.
"""


class PriceListViewList(LoginRequiredMixin, ListView):
    context_object_name = "pricelists"
    model = PriceList
    template_name = "price_list/pricelist_list.html"

    def get_context_data(self, **kwargs):
        context = super(PriceListViewList, self).get_context_data(**kwargs)
        context['can_create'] = len(PriceList.objects.all().filter(status=PRICE_LIST_PRE_RELEASE)) == 0
        return context


class PriceListViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'pricelist'
    model = PriceList
    template_name = "price_list/pricelist_detail.html"
    slug_url_kwarg = 'pl_id'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super(PriceListViewDetail, self).get_context_data(**kwargs)
        context['can_create'] = self.object.status == PRICE_LIST_PRE_RELEASE
        return context


class PriceListViewCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    context_object_name = 'pricelist'
    model = PriceList
    slug_field = 'id'
    slug_url_kwarg = 'pl_id'
    success_message = "%(name)s was created successfully!"
    template_name = "price_list/pricelist_form.html"
    form_class = PriceListForm

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        return context


class PriceListViewUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = 'pricelist'
    model = PriceList
    slug_field = 'id'
    slug_url_kwarg = 'pl_id'
    success_message = "%(name)s was updated successfully!"
    template_name = "price_list/pricelist_form.html"

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class PriceListViewDelete(LoginRequiredMixin, DeleteView):
    context_object_name = 'pricelist'
    model = PriceList
    slug_field = 'id'
    slug_url_kwarg = 'pl_id'
    success_url = reverse_lazy('pricelist_list')
    template_name = "price_list/pricelist_form.html"

    def get_context_data(self, **kwargs):
        context = super(PriceListViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context


"""
Activity Price list item model generic views.
"""


class ActivityPriceListItemViewCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    context_object_name = 'activityitem'
    model = ActivityPriceListItem
    template_name = "price_list/activity_pricelistitem_form.html"
    success_message = "%(name)s was created successfully!"
    form_class = ActivityPriceListItemForm

    def get_success_url(self):
        return reverse_lazy('activity_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class):
        return form_class(pl_id=self.kwargs['pl_id'], **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(ActivityPriceListItemViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        context['pricelist'] = get_object_or_404(PriceList, id=self.kwargs['pl_id'])
        return context


class ActivityPriceListItemViewUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = 'activityitem'
    model = ActivityPriceListItem
    success_message = "%(name)s was updated successfully!"
    template_name = "price_list/activity_pricelistitem_form.html"
    form_class = ActivityPriceListItemForm

    def get_success_url(self):
        return reverse_lazy('activity_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ActivityPriceListItemViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        context['pricelist'] = self.object.price_list
        return context


class ActivityPriceListItemViewDelete(LoginRequiredMixin, DeleteView):
    context_object_name = 'activityitem'
    model = ActivityPriceListItem
    template_name = "price_list/activity_pricelistitem_form.html"

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.price_list.pk})

    def get_context_data(self, **kwargs):
        context = super(ActivityPriceListItemViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        context['pricelist'] = self.object.price_list
        return context


class ActivityPriceListItemViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'activityitem'
    model = ActivityPriceListItem
    template_name = "price_list/activity_pricelistitem_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ActivityPriceListItemViewDetail, self).get_context_data(**kwargs)
        context['can_create'] = self.object.price_list.status == PRICE_LIST_PRE_RELEASE
        context['pricelist'] = self.object.price_list
        context['equipmentplir_set'] = PriceListItemEquipment.objects.filter(item_uuid=self.object.item_uuid,
                                                                             price_list=self.object.price_list)
        context['serviceplir_set'] = PriceListItemService.objects.filter(item_uuid=self.object.item_uuid,
                                                                         price_list=self.object.price_list)
        return context


"""
Price List Item Equipment Relation Model generic views.
"""


class PriceListItemEquipmentViewCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    context_object_name = 'equipmentplir'
    model = PriceListItemEquipment
    template_name = "price_list/equipment_pricelistitem_form.html"
    success_message = "'%(item_uuid)s: %(equipment)s x %(count)s' was added successfully!"
    form_class = PriceListItemEquipmentForm

    def get_form(self, form_class):
        return form_class(pl_id=self.kwargs['pl_id'], item_uuid=self.kwargs['item_uuid'], **self.get_form_kwargs())

    def get_success_url(self):
        return reverse_lazy('equipment_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListItemEquipmentViewCreate, self).get_context_data(**kwargs)
        context['pricelist'] = get_object_or_404(PriceList, pk=self.kwargs['pl_id'])
        return context


class PriceListItemEquipmentViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'equipmentplir'
    model = PriceListItemEquipment
    template_name = "price_list/equipment_pricelistitem_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PriceListItemEquipmentViewDetail, self).get_context_data(**kwargs)
        context['can_create'] = self.object.price_list.status == PRICE_LIST_PRE_RELEASE
        return context


class PriceListItemEquipmentViewUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = 'equipmentplir'
    model = PriceListItemEquipment
    template_name = "price_list/equipment_pricelistitem_form.html"
    success_message = "'%(item_uuid)s: %(equipment)s x %(count)s' was updated successfully!"
    form_class = PriceListItemEquipmentForm

    def get_success_url(self):
        return reverse_lazy('equipment_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListItemEquipmentViewUpdate, self).get_context_data(**kwargs)
        context['pricelist'] = self.object.price_list
        return context


class PriceListItemEquipmentViewDelete(LoginRequiredMixin, DeleteView):
    context_object_name = 'equipmentplir'
    model = PriceListItemEquipment
    template_name = "price_list/equipment_pricelistitem_form.html"

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pk': self.object.price_list.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListItemEquipmentViewDelete, self).get_context_data(**kwargs)
        context['pricelist'] = self.object.price_list
        return context


"""
Price List Item Service Relation Model generic views.
"""


class PriceListItemServiceViewCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    context_object_name = 'serviceplir'
    model = PriceListItemService
    template_name = "price_list/service_pricelistitem_form.html"
    success_message = "'%(item_uuid)s: %(service)s x %(count)s' was added successfully!"
    form_class = PriceListItemServiceForm

    def get_form(self, form_class):
        return form_class(pl_id=self.kwargs['pl_id'], item_uuid=self.kwargs['item_uuid'], **self.get_form_kwargs())

    def get_success_url(self):
        return reverse_lazy('service_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListItemServiceViewCreate, self).get_context_data(**kwargs)
        context['pricelist'] = get_object_or_404(PriceList, pk=self.kwargs['pl_id'])
        return context


class PriceListItemServiceViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'serviceplir'
    model = PriceListItemService
    template_name = "price_list/service_pricelistitem_detail.html"

    def get_context_data(self, **kwargs):
        context = super(PriceListItemServiceViewDetail, self).get_context_data(**kwargs)
        context['can_create'] = self.object.price_list.status == PRICE_LIST_PRE_RELEASE
        return context


class PriceListItemServiceViewUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = 'serviceplir'
    model = PriceListItemService
    template_name = "price_list/service_pricelistitem_form.html"
    success_message = "'%(item_uuid)s: %(service)s x %(count)s' was updated successfully!"
    form_class = PriceListItemServiceForm

    def get_success_url(self):
        return reverse_lazy('service_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListItemServiceViewUpdate, self).get_context_data(**kwargs)
        context['pricelist'] = self.object.price_list
        return context


class PriceListItemServiceViewDelete(LoginRequiredMixin, DeleteView):
    context_object_name = 'serviceplir'
    model = PriceListItemService
    template_name = "price_list/service_pricelistitem_form.html"

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.price_list.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListItemServiceViewDelete, self).get_context_data(**kwargs)
        context['pricelist'] = self.object.price_list
        return context
