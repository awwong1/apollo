from apps.price_list.forms import ActivityPriceListItemForm
from apps.price_list.models import PriceList, ActivityPriceListItem
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class PriceList_List(ListView):
    context_object_name = "pricelists"
    model = PriceList
    template_name = "price_list/pricelist_list.html"


class PriceList_Detail(DetailView):
    context_object_name = 'pricelist'
    model = PriceList
    template_name = "price_list/pricelist_detail.html"
    slug_url_kwarg = 'pl_id'
    slug_field = 'id'


class PriceList_Create(SuccessMessageMixin, CreateView):
    context_object_name = 'pricelist'
    model = PriceList
    template_name = "price_list/pricelist_create.html"
    success_message = "%(name)s was created successfully!"
    slug_url_kwarg = 'pl_id'
    slug_field = 'id'

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.pk})


class PriceList_Update(SuccessMessageMixin, UpdateView):
    context_object_name = 'pricelist'
    model = PriceList
    template_name = "price_list/pricelist_update.html"
    success_message = "%(name)s was updated successfully!"
    slug_url_kwarg = 'pl_id'
    slug_field = 'id'

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.pk})


class PriceList_Delete(SuccessMessageMixin, DeleteView):
    context_object_name = 'pricelist'
    model = PriceList
    template_name = "price_list/pricelist_delete.html"
    success_url = reverse_lazy('pricelist_list')
    success_message = "%(name)s was deleted successfully!"
    slug_url_kwarg = 'pl_id'
    slug_field = 'id'


class ActivityPriceListItem_Create(SuccessMessageMixin, CreateView):
    context_object_name = 'activityitem'
    model = ActivityPriceListItem
    template_name = "price_list/pricelist_create.html"
    success_message = "%(name)s was created successfully!"
    slug_url_kwarg = 'pl_id'
    slug_field = 'id'
    form_class = ActivityPriceListItemForm

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.pk})

    def get_form(self, form_class):
        pl_id = self.kwargs['pl_id']
        return ActivityPriceListItemForm()