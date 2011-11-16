# -*- encoding: utf-8 -*-

from studlan.competition.models import Activity, Competition
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def main(request):
    competitions = Competition.objects.all()
    activities = Activity.objects.all()

    for c in competitions:
        if len(c.desc) >= 200:
            c.desc = c.desc[:197] + '...'

    tab = request.GET.get('tab')
    if tab is None or tab == '': tab = 'all'

    return render_to_response('competitions.html', {'competitions': competitions, 'activities': activities, 'current_tab': tab},
                               context_instance=RequestContext(request))

def single(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)

    if not "http" in competition.activity.image_url:
        competition.activity.image_url = 'http://placehold.it/150x150'

    return render_to_response('competition.html', {'competition': competition},
							  context_instance=RequestContext(request))

def join(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    competition.participants.add(request.user)
    messages.add_message(request, messages.WARNING, 'You\'re now participating in %s.' % competition.title)
    return redirect('competition', competition_id=competition_id)

def leave(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    competition.participants.remove(request.user)
    messages.add_message(request, messages.WARNING, 'You\'re no longer participating in %s.' % competition.title)
    return redirect('competition', competition_id=competition_id)

def forfeit(request, competition_id):
    competition = get_object_or_404(Competition, pk=competition_id)
    messages.add_message(request, messages.ERROR, 'Forfeit not yet implemented!')
    return redirect('competition', competition_id=competition_id)

def log_in(request):
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'You\'ve successfully logged in.')
            else:
                messages.add_message(request, messages.WARNING, "Your account is not active, please try again or contact the site admin if the problem persists.")
        else:
            messages.add_message(request, messages.ERROR, "Wrong username/password.")
    return redirect('news')

def log_out(request):
    logout(request)

    #TODO cleanup
    messages.add_message(request, messages.SUCCESS, 'You\'ve successfully logged out.')
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

            #TODO cleanup
            messages.add_message(request, messages.SUCCESS, '<strong>Registration successful.</strong> You may now log in.')

    return redirect('news')
