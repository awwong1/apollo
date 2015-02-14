from apollo.viewmixins import LoginRequiredMixin, ActivitySendMixin
from applications.business.models import Business, BusinessMembership
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


class BusinessViewCreate(LoginRequiredMixin, SuccessMessageMixin, ActivitySendMixin, CreateView):
    context_object_name = "business"
    model = Business
    success_message = "%(name)s was created successfully!"
    template_name = "business/business_form.html"
    activity_verb = 'created business'
    fields = "__all__"

    def get_success_url(self):
        BusinessMembership.objects.create(user=self.request.user, business=self.object)
        return reverse_lazy('business_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(BusinessViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        return context


class BusinessViewList(LoginRequiredMixin, ListView):
    context_object_name = "businesses"
    model = Business
    template_name = "business/business_list.html"


class BusinessViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = "business"
    model = Business
    template_name = "business/business_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BusinessViewDetail, self).get_context_data(**kwargs)
        context['business_editable'] = len(self.object.businessmembership_set.all().filter(user=self.request.user)) > 0
        return context


class BusinessViewUpdate(LoginRequiredMixin, SuccessMessageMixin, ActivitySendMixin, UpdateView):
    context_object_name = "business"
    model = Business
    success_message = "%(name)s was updated successfully!"
    template_name = "business/business_form.html"
    activity_verb = 'updated business'
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy('business_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(BusinessViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class BusinessViewDelete(LoginRequiredMixin, DeleteView):
    context_object_name = 'business'
    model = Business
    success_url = reverse_lazy('business_list')
    template_name = "business/business_form.html"

    def get_context_data(self, **kwargs):
        context = super(BusinessViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context
