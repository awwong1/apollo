from apollo.choices import PRICE_LIST_PRE_RELEASE
from apollo.viewmixins import LoginRequiredMixin
from apps.price_list.forms import ActivityPriceListItemForm, PriceListForm
from apps.price_list.models import PriceList, ActivityPriceListItem
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


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

    def get_success_url(self):
        return reverse_lazy('activity_pricelistitem_detail', kwargs={'pk': self.object.pk})

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
        return context