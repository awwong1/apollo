from apollo.choices import PRICE_LIST_PRE_RELEASE
from apps.price_list.forms import ActivityPriceListItemForm, PriceListForm
from apps.price_list.models import PriceList, ActivityPriceListItem
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class PriceListViewList(ListView):
    context_object_name = "pricelists"
    model = PriceList
    template_name = "price_list/pricelist_list.html"

    def get_context_data(self, **kwargs):
        context = super(PriceListViewList, self).get_context_data(**kwargs)
        context['can_create'] = PriceList.objects.all().filter(status=PRICE_LIST_PRE_RELEASE) == 0
        return context


class PriceListViewDetail(DetailView):
    context_object_name = 'pricelist'
    model = PriceList
    template_name = "price_list/pricelist_detail.html"
    slug_url_kwarg = 'pl_id'
    slug_field = 'id'

    def get_context_data(self, **kwargs):
        context = super(PriceListViewDetail, self).get_context_data(**kwargs)
        context['can_create'] = self.object.status == PRICE_LIST_PRE_RELEASE
        return context


class PriceListViewCreate(SuccessMessageMixin, CreateView):
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


class PriceListViewUpdate(SuccessMessageMixin, UpdateView):
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


class PriceListViewDelete(DeleteView):
    context_object_name = 'pricelist'
    model = PriceList
    slug_field = 'id'
    slug_url_kwarg = 'pl_id'
    success_url = reverse_lazy('pricelist_list')
    template_name = "price_list/pricelist_form.html"

    def get_context_data(self, **kwargs):
        context = super(PriceListViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context


class ActivityPriceListItemViewCreate(SuccessMessageMixin, CreateView):
    context_object_name = 'activityitem'
    model = ActivityPriceListItem
    template_name = "price_list/activity_pricelistitem_form.html"
    success_message = "%(name)s was created successfully!"
    form_class = ActivityPriceListItemForm

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.pk})

    def get_form(self, form_class):
        pl_id = self.kwargs['pl_id']
        return ActivityPriceListItemForm(price_list_id=pl_id)

    def get_context_data(self, **kwargs):
        context = super(ActivityPriceListItemViewCreate, self).get_context_data(**kwargs)
        context['pricelist'] = get_object_or_404(PriceList, id=self.kwargs['pl_id'])
        context['action'] = "Create New"
        return context