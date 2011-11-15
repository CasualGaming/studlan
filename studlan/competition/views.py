# -*- encoding: utf-8 -*-

from studlan.competition.models import Activity, Competition
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def main(request):
    competitions = Competition.objects.all()

    for c in competitions:
        if len(c.desc) >= 200:
            c.desc = c.desc[:197] + '...'

    return render_to_response('competitions.html', {'competitions': competitions},
                               context_instance=RequestContext(request))

def single(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    
    statuses = {
        1: ['Registration open', 'success'],
        2: ['Registration closed', 'danger'],
        3: ['Competition in progress', 'warning'],
        4: ['Competition finished', 'info']
    }

    # 0 = status, 1 = label
    competition.status_text = statuses[competition.status][0]
    competition.status_label = statuses[competition.status][1]
    
    return render_to_response('competition.html', {'competition': competition},
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
    return redirect('news')

def log_out(request):
    logout(request)
    return redirect('news')

def register_user(request):
    
    username = password = fname = lname = email = ''
    if request.POST:
        uname       = request.POST.get('username')
        pword       = request.POST.get('password')
        fname       = request.POST.get('fname')
        lname       = request.POST.get('lname')
        email       = request.POST.get('email')
        if uname is not None and pword is not None and fname is not None and lname is not None and email is not None:
            user = User.objects.create_user(username=uname,
                                            password=pword,
                                            email=email)
            user.set_password(pword)
            user.first_name = fname
            user.last_name = lname
            user.is_active = True
            user.save()

    return redirect('news')
