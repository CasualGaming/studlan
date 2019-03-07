# -*- encoding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation


# This is accessed asynchronously to remove alerts via jquery
def remove_alert(request):
    try:
        pass
    except:
        pass
    return HttpResponse('')


def handler404(request):
    return render(request, '404.html')


def change_language(request):
    if request.method == "POST":
        user_language = request.POST["language"]
        translation.activate(user_language)
        request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
