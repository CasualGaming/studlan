# -*- encoding: utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.http import Http404

# This is accessed asynchronously to remove alerts via jquery
def remove_alert(request):
    try:
        pass
    except:
        pass
    return HttpResponse('')

def handler404(request):
    return render_to_response('404.html', context_instance=RequestContext(request))
