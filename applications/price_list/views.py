from apollo.choices import PRICE_LIST_PRE_RELEASE
from apollo.viewmixins import LoginRequiredMixin, ActivitySendMixin, StaffRequiredMixin
from applications.price_list.forms import ActivityPriceListItemForm, PriceListForm, PriceListItemEquipmentForm, \
    PriceListItemServiceForm, TimePriceListItemForm, UnitPriceListItemForm
from applications.price_list.models import PriceList, ActivityPriceListItem, PriceListItemEquipment, \
    PriceListItemService, \
    TimePriceListItem, UnitPriceListItem
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def PriceListItemRedirect(request, pl_id=None, item_uuid=None):
    """
    Given a price list item id and an item guid, redirect to the price list item detail page.
    If the item does not exist with the specified parameters, throw a 404 exception.
    """
    price_list = get_object_or_404(PriceList, pk=pl_id)
    item = price_list.get_item_from_uuid(item_uuid)
    if isinstance(item, ActivityPriceListItem):
        return redirect('activity_pricelistitem_detail', pk=item.pk)
    elif isinstance(item, TimePriceListItem):
        return redirect('time_pricelistitem_detail', pk=item.pk)
    elif isinstance(item, UnitPriceListItem):
        return redirect('unit_pricelistitem_detail', pk=item.pk)
    raise Http404("No item exists for pl: {pl_id} and item uuid: {item_uuid}".format(pl_id=pl_id, item_uuid=item_uuid))


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


class PriceListViewCreate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin, CreateView):
    context_object_name = 'pricelist'
    model = PriceList
    slug_field = 'id'
    slug_url_kwarg = 'pl_id'
    success_message = "%(name)s was created successfully!"
    template_name = "price_list/pricelist_form.html"
    form_class = PriceListForm
    activity_verb = 'created price list'

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        return context


class PriceListViewUpdate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin, UpdateView):
    context_object_name = 'pricelist'
    model = PriceList
    slug_field = 'id'
    slug_url_kwarg = 'pl_id'
    success_message = "%(name)s was updated successfully!"
    template_name = "price_list/pricelist_form.html"
    activity_verb = 'updated price list'
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class PriceListViewDelete(LoginRequiredMixin, StaffRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'pricelist'
    model = PriceList
    slug_field = 'id'
    slug_url_kwarg = 'pl_id'
    success_url = reverse_lazy('pricelist_list')
    template_name = "price_list/pricelist_form.html"
    activity_verb = 'deleted price list'
    target_object_valid = False

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super(PriceListViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context


"""
Activity Price list item model generic views.
"""


class ActivityPriceListItemViewCreate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin,
                                      CreateView):
    context_object_name = 'activityitem'
    model = ActivityPriceListItem
    template_name = "price_list/activity_pricelistitem_form.html"
    success_message = "%(name)s was created successfully!"
    form_class = ActivityPriceListItemForm
    activity_verb = 'created activity price list item'

    def get_success_url(self):
        return reverse_lazy('activity_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class):
        return form_class(pl_id=self.kwargs['pl_id'], **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(ActivityPriceListItemViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        context['pricelist'] = get_object_or_404(PriceList, id=self.kwargs['pl_id'])
        return context


class ActivityPriceListItemViewUpdate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin,
                                      UpdateView):
    context_object_name = 'activityitem'
    model = ActivityPriceListItem
    success_message = "%(name)s was updated successfully!"
    template_name = "price_list/activity_pricelistitem_form.html"
    form_class = ActivityPriceListItemForm
    activity_verb = 'updated activity price list item'

    def get_success_url(self):
        return reverse_lazy('activity_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ActivityPriceListItemViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        context['pricelist'] = self.object.price_list
        return context


class ActivityPriceListItemViewDelete(LoginRequiredMixin, StaffRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'activityitem'
    model = ActivityPriceListItem
    template_name = "price_list/activity_pricelistitem_form.html"
    target_object_valid = False
    activity_verb = 'deleted activity price list item'

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
Time Price list item model generic views.
"""


class TimePriceListItemViewCreate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin,
                                  CreateView):
    context_object_name = 'timeitem'
    model = TimePriceListItem
    template_name = "price_list/time_pricelistitem_form.html"
    success_message = "%(name)s was created successfully!"
    form_class = TimePriceListItemForm
    activity_verb = 'created time price list item'

    def get_success_url(self):
        return reverse_lazy('time_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class):
        return form_class(pl_id=self.kwargs['pl_id'], **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(TimePriceListItemViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        context['pricelist'] = get_object_or_404(PriceList, id=self.kwargs['pl_id'])
        return context


class TimePriceListItemViewUpdate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin,
                                  UpdateView):
    context_object_name = 'timeitem'
    model = TimePriceListItem
    success_message = "%(name)s was updated successfully!"
    template_name = "price_list/time_pricelistitem_form.html"
    form_class = TimePriceListItemForm
    activity_verb = 'updated time price list item'

    def get_success_url(self):
        return reverse_lazy('time_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(TimePriceListItemViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        context['pricelist'] = self.object.price_list
        return context


class TimePriceListItemViewDelete(LoginRequiredMixin, StaffRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'timeitem'
    model = TimePriceListItem
    template_name = "price_list/time_pricelistitem_form.html"
    activity_verb = 'deleted time price list item'
    target_object_valid = False

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.price_list.pk})

    def get_context_data(self, **kwargs):
        context = super(TimePriceListItemViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        context['pricelist'] = self.object.price_list
        return context


class TimePriceListItemViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'timeitem'
    model = TimePriceListItem
    template_name = "price_list/time_pricelistitem_detail.html"

    def get_context_data(self, **kwargs):
        context = super(TimePriceListItemViewDetail, self).get_context_data(**kwargs)
        context['can_create'] = self.object.price_list.status == PRICE_LIST_PRE_RELEASE
        context['pricelist'] = self.object.price_list
        context['equipmentplir_set'] = PriceListItemEquipment.objects.filter(item_uuid=self.object.item_uuid,
                                                                             price_list=self.object.price_list)
        context['serviceplir_set'] = PriceListItemService.objects.filter(item_uuid=self.object.item_uuid,
                                                                         price_list=self.object.price_list)
        return context


"""
Unit Price list item model generic views.
"""


class UnitPriceListItemViewCreate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin,
                                  CreateView):
    context_object_name = 'unititem'
    model = UnitPriceListItem
    template_name = "price_list/unit_pricelistitem_form.html"
    success_message = "%(name)s was created successfully!"
    form_class = UnitPriceListItemForm
    activity_verb = 'created unit price list item'

    def get_success_url(self):
        return reverse_lazy('unit_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class):
        return form_class(pl_id=self.kwargs['pl_id'], **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(UnitPriceListItemViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        context['pricelist'] = get_object_or_404(PriceList, id=self.kwargs['pl_id'])
        return context


class UnitPriceListItemViewUpdate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin,
                                  UpdateView):
    context_object_name = 'unititem'
    model = UnitPriceListItem
    success_message = "%(name)s was updated successfully!"
    template_name = "price_list/unit_pricelistitem_form.html"
    form_class = UnitPriceListItemForm
    activity_verb = 'updated unit price list item'

    def get_success_url(self):
        return reverse_lazy('unit_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(UnitPriceListItemViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        context['pricelist'] = self.object.price_list
        return context


class UnitPriceListItemViewDelete(LoginRequiredMixin, StaffRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'unititem'
    model = UnitPriceListItem
    template_name = "price_list/unit_pricelistitem_form.html"
    activity_verb = 'deleted unit price list item'
    target_object_valid = False

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.price_list.pk})

    def get_context_data(self, **kwargs):
        context = super(UnitPriceListItemViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        context['pricelist'] = self.object.price_list
        return context


class UnitPriceListItemViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'unititem'
    model = UnitPriceListItem
    template_name = "price_list/unit_pricelistitem_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UnitPriceListItemViewDetail, self).get_context_data(**kwargs)
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


class PriceListItemEquipmentViewCreate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin,
                                       CreateView):
    context_object_name = 'equipmentplir'
    model = PriceListItemEquipment
    template_name = "price_list/equipment_pricelistitem_form.html"
    success_message = "'%(item_uuid)s: %(equipment)s x %(count)s' was added successfully!"
    form_class = PriceListItemEquipmentForm
    activity_verb = 'created equipment price list item relation'

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


class PriceListItemEquipmentViewUpdate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin,
                                       UpdateView):
    context_object_name = 'equipmentplir'
    model = PriceListItemEquipment
    template_name = "price_list/equipment_pricelistitem_form.html"
    success_message = "'%(item_uuid)s: %(equipment)s x %(count)s' was updated successfully!"
    form_class = PriceListItemEquipmentForm
    activity_verb = 'updated equipment price list item relation'

    def get_success_url(self):
        return reverse_lazy('equipment_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListItemEquipmentViewUpdate, self).get_context_data(**kwargs)
        context['pricelist'] = self.object.price_list
        return context


class PriceListItemEquipmentViewDelete(LoginRequiredMixin, StaffRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'equipmentplir'
    model = PriceListItemEquipment
    template_name = "price_list/equipment_pricelistitem_form.html"
    activity_verb = 'deleted equipment price list item relation'
    target_object_valid = False

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pk': self.object.price_list.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListItemEquipmentViewDelete, self).get_context_data(**kwargs)
        context['pricelist'] = self.object.price_list
        return context


"""
Price List Item Service Relation Model generic views.
"""


class PriceListItemServiceViewCreate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin,
                                     CreateView):
    context_object_name = 'serviceplir'
    model = PriceListItemService
    template_name = "price_list/service_pricelistitem_form.html"
    success_message = "'%(item_uuid)s: %(service)s x %(count)s' was added successfully!"
    form_class = PriceListItemServiceForm
    activity_verb = 'created service price list item relation'

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


class PriceListItemServiceViewUpdate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin,
                                     UpdateView):
    context_object_name = 'serviceplir'
    model = PriceListItemService
    template_name = "price_list/service_pricelistitem_form.html"
    success_message = "'%(item_uuid)s: %(service)s x %(count)s' was updated successfully!"
    form_class = PriceListItemServiceForm
    activity_verb = 'updated service price list item relation'

    def get_success_url(self):
        return reverse_lazy('service_pricelistitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListItemServiceViewUpdate, self).get_context_data(**kwargs)
        context['pricelist'] = self.object.price_list
        return context


class PriceListItemServiceViewDelete(LoginRequiredMixin, StaffRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'serviceplir'
    model = PriceListItemService
    template_name = "price_list/service_pricelistitem_form.html"
    target_object_valid = False
    activity_verb = 'deleted service price list item relation'

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.price_list.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceListItemServiceViewDelete, self).get_context_data(**kwargs)
        context['pricelist'] = self.object.price_list
        return context
