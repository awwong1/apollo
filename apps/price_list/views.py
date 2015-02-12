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
    slug_field = 'id'
    slug_url_kwarg = 'pl_id'
    success_message = "%(name)s was created successfully!"
    template_name = "price_list/pricelist_form.html"

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceList_Create, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        return context


class PriceList_Update(SuccessMessageMixin, UpdateView):
    context_object_name = 'pricelist'
    model = PriceList
    slug_field = 'id'
    slug_url_kwarg = 'pl_id'
    success_message = "%(name)s was updated successfully!"
    template_name = "price_list/pricelist_form.html"

    def get_success_url(self):
        return reverse_lazy('pricelist_detail', kwargs={'pl_id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PriceList_Update, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class PriceList_Delete(DeleteView):
    context_object_name = 'pricelist'
    model = PriceList
    slug_field = 'id'
    slug_url_kwarg = 'pl_id'
    success_url = reverse_lazy('pricelist_list')
    template_name = "price_list/pricelist_form.html"

    def get_context_data(self, **kwargs):
        context = super(PriceList_Create, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context


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