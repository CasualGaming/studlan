# -*- encoding: utf-8 -*-

from studlan.news.models import Article
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout

def main(request):
    articles = Article.objects.all()
    state = "Please log in below"
    return render_to_response('news.html', {'state':state, 'news':articles},
                              context_instance=RequestContext(request))

def log_in(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
        else:
            state = "Your account is not active, please contact the site admin."
    else:
        state = "Your username and/or password were incorrect."
    articles = Article.objects.all()
    return render_to_response('news.html', {'state':state, 'news':articles, 'username':username},
                             context_instance=RequestContext(request))

def log_out(request):
    logout(request)
    return redirect('news')
