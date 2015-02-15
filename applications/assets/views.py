from apollo.viewmixins import LoginRequiredMixin, ActivitySendMixin, StaffRequiredMixin
from applications.assets.models import Equipment, Service
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class EquipmentViewList(LoginRequiredMixin, ListView):
    context_object_name = "equipment"
    model = Equipment
    template_name = "equipment/equipment_list.html"


class EquipmentViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'equipment'
    model = Equipment
    template_name = "equipment/equipment_detail.html"


class EquipmentViewCreate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin, CreateView):
    context_object_name = 'equipment'
    model = Equipment
    success_message = "%(name)s was created successfully!"
    template_name = "equipment/equipment_form.html"
    activity_verb = 'created equipment'
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy('equipment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(EquipmentViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        return context


class EquipmentViewUpdate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin, UpdateView):
    context_object_name = 'equipment'
    model = Equipment
    success_message = "%(name)s was updated successfully!"
    template_name = "equipment/equipment_form.html"
    activity_verb = 'updated equipment'
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy('equipment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(EquipmentViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class EquipmentViewDelete(LoginRequiredMixin, StaffRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'equipment'
    model = Equipment
    success_url = reverse_lazy('equipment_list')
    template_name = "equipment/equipment_form.html"
    activity_verb = 'deleted equipment'
    target_object_valid = False

    def get_context_data(self, **kwargs):
        context = super(EquipmentViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context


class ServiceViewList(LoginRequiredMixin, ListView):
    context_object_name = "services"
    model = Service
    template_name = "service/service_list.html"


class ServiceViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'service'
    model = Service
    template_name = "service/service_detail.html"


class ServiceViewCreate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin, CreateView):
    context_object_name = 'service'
    model = Service
    success_message = "%(name)s was created successfully!"
    template_name = "service/service_form.html"
    activity_verb = 'created service'
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy('service_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ServiceViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        return context


class ServiceViewUpdate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, ActivitySendMixin, UpdateView):
    context_object_name = 'service'
    model = Service
    success_message = "%(name)s was updated successfully!"
    template_name = "service/service_form.html"
    activity_verb = 'updated service'
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy('service_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ServiceViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class ServiceViewDelete(LoginRequiredMixin, StaffRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'service'
    model = Service
    success_url = reverse_lazy('service_list')
    template_name = "service/service_form.html"
    activity_verb = 'deleted service'
    target_object_valid = False

    def get_context_data(self, **kwargs):
        context = super(ServiceViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context