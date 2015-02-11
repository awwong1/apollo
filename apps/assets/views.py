from apps.assets.models import Equipment
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class EquipmentViewList(ListView):
    context_object_name = "equipment"
    model = Equipment
    template_name = "equipment/equipment_list.html"


class EquipmentViewDetail(DetailView):
    context_object_name = 'equipment'
    model = Equipment
    template_name = "equipment/equipment_detail.html"


class EquipmentViewCreate(SuccessMessageMixin, CreateView):
    context_object_name = 'equipment'
    model = Equipment
    success_message = "%(name)s was created successfully!"
    template_name = "equipment/equipment_form.html"

    def get_success_url(self):
        return reverse_lazy('equipment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(EquipmentViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        return context


class EquipmentViewUpdate(SuccessMessageMixin, UpdateView):
    context_object_name = 'equipment'
    model = Equipment
    success_message = "%(name)s was updated successfully!"
    template_name = "equipment/equipment_form.html"

    def get_success_url(self):
        return reverse_lazy('equipment_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(EquipmentViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class EquipmentViewDelete(DeleteView):
    context_object_name = 'equipment'
    model = Equipment
    success_url = reverse_lazy('equipment_list')
    template_name = "equipment/equipment_form.html"

    def get_context_data(self, **kwargs):
        context = super(EquipmentViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context