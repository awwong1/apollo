from apollo.viewmixins import LoginRequiredMixin, StaffRequiredMixin
from applications.terms_of_service.models import TermsOfService
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class TermsOfServiceViewList(LoginRequiredMixin, ListView):
    context_object_name = "termsofservices"
    model = TermsOfService
    template_name = "terms_of_service/termsofservice_list.html"


class TermsOfServiceViewDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'termsofservice'
    model = TermsOfService
    template_name = "terms_of_service/termsofservice_detail.html"


class TermsOfServiceViewCreate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, CreateView):
    context_object_name = 'termsofservice'
    model = TermsOfService
    success_message = "%(title)s was created successfully!"
    template_name = "terms_of_service/termsofservice_form.html"

    def get_success_url(self):
        return reverse_lazy('termsofservice_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(TermsOfServiceViewCreate, self).get_context_data(**kwargs)
        context['action'] = "Create New"
        return context


class TermsOfServiceViewUpdate(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    context_object_name = 'termsofservice'
    model = TermsOfService
    success_message = "%(title)s was updated successfully!"
    template_name = "terms_of_service/termsofservice_form.html"

    def get_success_url(self):
        return reverse_lazy('termsofservice_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(TermsOfServiceViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class TermsOfServiceViewDelete(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    context_object_name = 'termsofservice'
    model = TermsOfService
    success_url = reverse_lazy('termsofservice_list')
    template_name = "terms_of_service/termsofservice_form.html"

    def get_context_data(self, **kwargs):
        context = super(TermsOfServiceViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context