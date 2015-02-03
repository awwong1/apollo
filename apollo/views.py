from django.shortcuts import render_to_response
from django.template import RequestContext


def base(request):
    if request.user.is_authenticated():
        return render_to_response('base.html', {}, context_instance=RequestContext(request))
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