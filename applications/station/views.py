from apollo.choices import CHARGE_LIST_OPEN
from apollo.viewmixins import LoginRequiredMixin, ActivitySendMixin, StaffRequiredMixin
from applications.business.models import Business
from applications.charge_list.forms import ActivityChargeCatalog, TimeChargeCatalog, UnitChargeCatalog
from applications.charge_list.models import ChargeList
from applications.station.forms import StationBusinessForm
from applications.station.models import Station, StationBusiness
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


def StationUUIDRedirect(request, station_uuid=None):
    """
    Given a station guid, redirect to the station detail page.
    If the station does not exist with the specified parameters, throw a 404 exception.
    """
    station = get_object_or_404(Station, uuid=station_uuid)
    return redirect('station_detail', kwargs={'pk': station.pk})


"""
Station model generic views.
"""


class StationViewList(LoginRequiredMixin, ListView):
    context_object_name = "stations"
    model = Station
    template_name = "station/station_list.html"

    def get_context_data(self, **kwargs):
        context = super(StationViewList, self).get_context_data(**kwargs)
        return context


class StationViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'station'
    model = Station
    template_name = "station/station_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StationViewDetail, self).get_context_data(**kwargs)
        user_businesses = Business.objects.filter(businessmembership__user=self.request.user)
        station_businesses = self.object.stationbusiness_set.all()
        context['can_modify'] = station_businesses.filter(business__in=user_businesses)
        active_cl = ChargeList.objects.filter(station=self.object, status=CHARGE_LIST_OPEN)
        if len(active_cl) == 1:
            context['chargelist'] = active_cl[0]
            if context['can_modify']:
                price_list_pk = active_cl[0].price_list.pk
                context['activitycharge_catalog'] = ActivityChargeCatalog(price_list_pk=price_list_pk)
                context['timecharge_catalog'] = TimeChargeCatalog(price_list_pk=price_list_pk)
                context['unitcharge_catalog'] = UnitChargeCatalog(price_list_pk=price_list_pk)
        return context


class StationViewCreate(LoginRequiredMixin, SuccessMessageMixin, ActivitySendMixin, CreateView):
    context_object_name = 'station'
    model = Station
    success_message = "%(name)s was created successfully!"
    template_name = "station/station_form.html"
    activity_verb = 'created station'
    fields = "__all__"

    def dispatch(self, *args, **kwargs):
        business = get_object_or_404(Business, pk=self.kwargs.get('business_pk', '-1'))
        user_businesses = self.request.user.businessmembership_set.all()
        can_modify = user_businesses.filter(business=business)
        if can_modify:
            return super(StationViewCreate, self).dispatch(*args, **kwargs)
        else:
            messages.warning(self.request, "You do not have permissions to create a station for this business.")
            return redirect('business_detail', pk=business.pk)

    def get_success_url(self):
        business = get_object_or_404(Business, pk=self.kwargs.get('business_pk', '-1'))
        StationBusiness.objects.create(business=business, station=self.object)
        return reverse_lazy('station_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(StationViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        return context


class StationViewUpdate(LoginRequiredMixin, SuccessMessageMixin, ActivitySendMixin, UpdateView):
    context_object_name = 'station'
    model = Station
    success_message = "%(name)s was updated successfully!"
    template_name = "station/station_form.html"
    activity_verb = 'updated station'
    fields = "__all__"

    def dispatch(self, *args, **kwargs):
        station = get_object_or_404(Station, pk=self.kwargs.get('pk', '-1'))
        user_businesses = self.request.user.businessmembership_set.all()
        can_modify = station.stationbusiness_set.all().filter(business__in=user_businesses)
        if can_modify:
            return super(StationViewUpdate, self).dispatch(*args, **kwargs)
        else:
            messages.warning(self.request, "You do not have permissions to update this station.")
            return redirect('station_detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('station_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(StationViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class StationViewDelete(LoginRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'station'
    model = Station
    success_url = reverse_lazy('base')
    template_name = "station/station_form.html"
    activity_verb = 'deleted station'
    target_object_valid = False

    def dispatch(self, *args, **kwargs):
        station = get_object_or_404(Station, pk=self.kwargs.get('pk', '-1'))
        user_businesses = self.request.user.businessmembership_set.all()
        can_modify = station.stationbusiness_set.all().filter(business__in=user_businesses)
        if can_modify:
            return super(StationViewDelete, self).dispatch(*args, **kwargs)
        else:
            messages.warning(self.request, "You do not have permissions to delete this station.")
            return redirect('station_detail', pk=station.pk)

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        context = super(StationViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context


"""
Station Business Association generic views
"""


class StationBusinessViewCreate(LoginRequiredMixin, SuccessMessageMixin, ActivitySendMixin, CreateView):
    context_object_name = 'stationbusiness'
    model = StationBusiness
    template_name = "station/stationbusiness_form.html"
    activity_verb = 'created station business association'
    success_message = "%(station)s: %(business)s relation successfully created!"
    form_class = StationBusinessForm

    def dispatch(self, *args, **kwargs):
        station = get_object_or_404(Station, pk=self.kwargs.get('station_pk', '-1'))
        user_businesses = self.request.user.businessmembership_set.all()
        can_modify = station.stationbusiness_set.all().filter(business__in=user_businesses)
        if can_modify:
            return super(StationBusinessViewCreate, self).dispatch(*args, **kwargs)
        else:
            messages.warning(self.request, "You do not have permissions to create this station business.")
            return redirect('station_detail', pk=station.pk)

    def get_form(self, form_class):
        return form_class(station_pk=self.kwargs['station_pk'], **self.get_form_kwargs())

    def get_success_url(self):
        return reverse_lazy('station_detail', pk=self.kwargs['station_pk'])

    def get_context_data(self, **kwargs):
        context = super(StationBusinessViewCreate, self).get_context_data(**kwargs)
        context['station'] = Station.objects.get(pk=self.kwargs['station_pk'])
        return context


class StationBusinessViewDelete(LoginRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'stationbusiness'
    model = StationBusiness
    template_name = "station/stationbusiness_form.html"
    activity_verb = 'deleted station business association'
    target_object_valid = False

    def get_success_url(self):
        return reverse_lazy('station_detail', kwargs={'pk': self.object.station.pk})

    def dispatch(self, *args, **kwargs):
        stationbusiness = get_object_or_404(StationBusiness, pk=self.kwargs.get('pk', '-1'))
        business = stationbusiness.business
        station = stationbusiness.station
        user_businesses = self.request.user.businessmembership_set.all()
        can_modify = business.stationbusiness_set.all().filter(business__in=user_businesses)
        last_business = len(station.stationbusiness_set.all()) == 1
        if can_modify:
            if last_business:
                messages.warning(self.request, "You cannot delete the last station business for this station!")
                return redirect('station_detail', pk=station.pk)
            return super(StationBusinessViewDelete, self).dispatch(*args, **kwargs)
        else:
            messages.warning(self.request, "You do not have permissions to delete this a station business.")
            return redirect('station_detail', pk=station.pk)

    def get_context_data(self, **kwargs):
        context = super(StationBusinessViewDelete, self).get_context_data(**kwargs)
        context['station'] = self.object.station
        return context
