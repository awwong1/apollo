from apollo.viewmixins import LoginRequiredMixin, ActivitySendMixin
from applications.business.forms import BusinessMembershipForm
from applications.business.models import Business, BusinessMembership
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView


"""
Business Generic Views
"""


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

    def dispatch(self, *args, **kwargs):
        business = get_object_or_404(Business, pk=self.kwargs['pk'])
        user_businesses = business.businessmembership_set.all().filter(user=self.request.user)
        can_modify = len(user_businesses) == 1
        if can_modify:
            return super(BusinessViewUpdate, self).dispatch(*args, **kwargs)
        else:
            messages.warning(self.request, "You do not have permissions to update this business.")
            return redirect('business_detail', pk=business.pk)

    def get_success_url(self):
        return reverse_lazy('business_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(BusinessViewUpdate, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class BusinessViewDelete(LoginRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'business'
    model = Business
    success_url = reverse_lazy('base')
    template_name = "business/business_form.html"
    activity_verb = 'deleted business'
    target_object_valid = False

    def dispatch(self, *args, **kwargs):
        business = get_object_or_404(Business, pk=self.kwargs['pk'])
        user_businesses = business.businessmembership_set.all().filter(user=self.request.user)
        can_modify = len(user_businesses) == 1
        if can_modify:
            return super(BusinessViewDelete, self).dispatch(*args, **kwargs)
        else:
            messages.warning(self.request, "You do not have permissions to delete this business.")
            return redirect('business_detail', pk=business.pk)

    def get_context_data(self, **kwargs):
        context = super(BusinessViewDelete, self).get_context_data(**kwargs)
        context['action'] = "Delete"
        return context


"""
Business Membership Generic Views
"""


class BusinessMembershipViewCreate(LoginRequiredMixin, ActivitySendMixin, SuccessMessageMixin, CreateView):
    context_object_name = 'businessmembership'
    model = BusinessMembership
    form_class = BusinessMembershipForm
    template_name = 'business/businessmembership_form.html'
    activity_verb = 'created business membership'
    success_message = '"%(business)s: %(user)s was created successfully!"'

    def dispatch(self, *args, **kwargs):
        business = get_object_or_404(Business, pk=self.kwargs.get('business_pk', '-1'))
        not_member = len(business.businessmembership_set.all().filter(user=self.request.user)) != 1
        if not_member:
            messages.warning(self.request, "You do not have permissions to create a membership for this business.")
            return redirect('business_detail', pk=business.pk)
        else:
            return super(BusinessMembershipViewCreate, self).dispatch(*args, **kwargs)

    def get_form(self, form_class):
        return form_class(business_pk=self.kwargs['business_pk'], **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(BusinessMembershipViewCreate, self).get_context_data(**kwargs)
        context['business'] = get_object_or_404(Business, pk=self.kwargs['business_pk'])
        context['action'] = 'Create'
        return context

    def get_success_url(self):
        return reverse_lazy('business_detail', kwargs={'pk': self.object.business.pk})


class BusinessMembershipViewDelete(LoginRequiredMixin, ActivitySendMixin, DeleteView):
    context_object_name = 'businessmembership'
    model = BusinessMembership
    template_name = 'business/businessmembership_form.html'
    activity_verb = 'deleted business membership'
    target_object_valid = False

    def dispatch(self, *args, **kwargs):
        business = get_object_or_404(BusinessMembership, pk=kwargs.get('pk', '-1')).business
        members = business.businessmembership_set.all()
        not_member = len(members.filter(user=self.request.user)) != 1
        if not_member:
            messages.warning(self.request, "You do not have permissions to delete a membership for this business.")
            return redirect('business_detail', pk=business.pk)
        elif len(members) == 1:
            messages.warning(self.request, "You cannot delete the last membership in a business.")
            return redirect('business_detail', pk=business.pk)
        else:
            return super(BusinessMembershipViewDelete, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('business_detail', kwargs={'pk': self.object.business.pk})

    def get_context_data(self, **kwargs):
        context = super(BusinessMembershipViewDelete, self).get_context_data(**kwargs)
        context['business'] = self.object.business
        context['action'] = 'Delete'
        return context