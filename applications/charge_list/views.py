from apollo.choices import CHARGE_LIST_OPEN
from apollo.viewmixins import LoginRequiredMixin, ActivitySendMixin
from applications.charge_list.forms import ChargeListForm
from applications.charge_list.models import ChargeList
from applications.station.models import Station
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView


class ChargeListViewCreate(LoginRequiredMixin, ActivitySendMixin, CreateView):
    context_object_name = 'chargelist'
    model = ChargeList
    template_name = 'charge_list/chargelist_form.html'
    form_class = ChargeListForm
    activity_verb = "created charge list"

    def dispatch(self, *args, **kwargs):
        station = get_object_or_404(Station, pk=self.kwargs.get('station_pk', '-1'))
        user_businesses = self.request.user.businessmembership_set.all()
        can_modify = station.stationbusiness_set.all().filter(business__in=user_businesses)
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
