from apollo.choices import CHARGE_LIST_OPEN
from apollo.viewmixins import LoginRequiredMixin, ActivitySendMixin
from applications.business.models import Business
from applications.charge_list.forms import ChargeListForm, ActivityChargeForm
from applications.charge_list.models import ChargeList, ActivityCharge
from applications.price_list.models import ActivityPriceListItem
from applications.station.models import Station
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView


class ChargeListViewCreate(LoginRequiredMixin, SuccessMessageMixin, ActivitySendMixin, CreateView):
    context_object_name = 'chargelist'
    model = ChargeList
    template_name = 'charge_list/chargelist_form.html'
    form_class = ChargeListForm
    success_message = "Charge List successfully created!"
    activity_verb = "created charge list"

    def dispatch(self, *args, **kwargs):
        station = get_object_or_404(Station, pk=self.kwargs.get('station_pk', '-1'))
        station_businesses = station.stationbusiness_set.all()
        user_businesses = Business.objects.filter(businessmembership__user=self.request.user)
        can_modify = station_businesses.filter(business__in=user_businesses)
        if can_modify:
            if len(station.chargelist_set.all().filter(status=CHARGE_LIST_OPEN)) > 0:
                messages.warning(self.request, "An open charge list already exists for this business.")
                return redirect('station_detail', pk=station.pk)
            return super(ChargeListViewCreate, self).dispatch(*args, **kwargs)
        else:
            messages.warning(self.request, "You do not have permissions to create a charge list for this station.")
            return redirect('station_detail', pk=station.pk)

    def get_form(self, form_class):
        return form_class(station_pk=self.kwargs['station_pk'], **self.get_form_kwargs())

    def get_success_url(self):
        return reverse_lazy('station_detail', kwargs={'pk': self.kwargs['station_pk']})

    def get_context_data(self, **kwargs):
        context = super(ChargeListViewCreate, self).get_context_data(**kwargs)
        context['station'] = Station.objects.get(pk=self.kwargs['station_pk'])
        return context


class ChargeListViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'chargelist'
    model = ChargeList
    template_name = 'charge_list/chargelist_detail.html'


class ChargeListViewList(LoginRequiredMixin, ListView):
    context_object_name = 'chargelists'
    model = ChargeList
    template_name = 'charge_list/chargelist_list.html'


"""
Activity Charge Item Generic Viewsets
"""


class ActivityChargeViewCreate(LoginRequiredMixin, ActivitySendMixin, SuccessMessageMixin, CreateView):
    """
    Requires url encoded chargelist_pk, get parameter activity_items=<ActivityPriceListItem.pk>
    """
    context_object_name = 'activitycharge'
    model = ActivityCharge
    template_name = 'charge_list/activitycharge_form.html'
    form_class = ActivityChargeForm
    activity_verb = 'created activity charge'
    success_message = '%(price_list_item)s successfully added!'

    def dispatch(self, *args, **kwargs):
        charge_list = get_object_or_404(ChargeList, pk=self.kwargs.get('chargelist_pk', '-1'))
        station = charge_list.station
        station_business = station.stationbusiness_set.all()
        businesses = Business.objects.filter(businessmembership__user=self.request.user)
        can_modify = station_business.filter(business__in=businesses)
        if can_modify:
            activity_item_pk = self.request.GET.get('activity_items', None)
            if activity_item_pk is None:
                messages.warning(self.request, "An activity item must be provided to add.")
                return redirect('station_detail', pk=station.pk)
            act_item = get_object_or_404(ActivityPriceListItem, pk=activity_item_pk)
            if act_item.price_list != charge_list.price_list:
                messages.warning(self.request, "The provided activity item must be part of the current price list.")
                return redirect('station_detail', pk=station.pk)
            return super(ActivityChargeViewCreate, self).dispatch(*args, **kwargs)
        else:
            messages.warning(self.request, "You do not have permissions to create a charge list for this station.")
            return redirect('station_detail', pk=station.pk)

    def get_form(self, form_class):
        return form_class(chargelist_pk=self.kwargs['chargelist_pk'], activitypli_pk=self.request.GET['activity_items'],
                          **self.get_form_kwargs())

    def get_success_url(self):
        charge_list = get_object_or_404(ChargeList, pk=self.kwargs.get('chargelist_pk', '-1'))
        station = charge_list.station
        return reverse_lazy('station_detail', kwargs={'pk': station.pk})

    def get_context_data(self, **kwargs):
        context = super(ActivityChargeViewCreate, self).get_context_data(**kwargs)
        charge_list = get_object_or_404(ChargeList, pk=self.kwargs.get('chargelist_pk', '-1'))
        context['station'] = charge_list.station
        return context


class TimeChargeViewCreate(LoginRequiredMixin, CreateView):
    pass


class UnitChargeViewCreate(LoginRequiredMixin, CreateView):
    pass