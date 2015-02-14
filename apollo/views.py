from actstream import action
from apollo.forms import ToggleStaffForm
from applications.business.models import Business
from django.contrib import messages
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def base(request):
    if request.user.is_authenticated():
        data = dict()
        data['businesses'] = Business.objects.filter(businessmembership__user=request.user)
        return render_to_response('business/business_home.html', data, context_instance=RequestContext(request))
    else:
        return base_idea(request)


def base_idea(request):
    return render_to_response('base/base_idea.html', {}, context_instance=RequestContext(request))


def base_prototype(request):
    return render_to_response('base/base_prototype.html', {}, context_instance=RequestContext(request))


def base_contact(request):
    return render_to_response('base/base_contact.html', {}, context_instance=RequestContext(request))


def ws_demo(request):
    return render_to_response('demo.html', {}, context_instance=RequestContext(request))


def toggle_staff_view(request):
    data = dict()
    if request.method == 'GET':
        data['form'] = ToggleStaffForm(instance=request.user)
    elif request.method == 'POST':
        form = ToggleStaffForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully edited your staff privileges.")
            action.send(request.user, verb='toggled staff mode {boolean}'.format(boolean=form.cleaned_data['is_staff']))
            return redirect('/')
    return render_to_response('account/toggle_staff.html', data, context_instance=RequestContext(request))
