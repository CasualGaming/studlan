# -*- encoding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import translation


# This is accessed asynchronously to remove alerts via jquery
def remove_alert(request):
    return HttpResponse('')


def handler404(request):
    return render_to_response('404.html', context_instance=RequestContext(request))


def change_language(request):
    if request.method == 'POST':
        user_language = request.POST['language']
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
