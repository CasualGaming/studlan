# -*- encoding: utf-8 -*-

from studlan.competition.models import Activity, Competition
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth import authenticate, login, logout

def main(request):
	competitions = Competition.objects.all()

	for c in competitions:
		if len(c.desc) >= 200:
			c.desc = c.desc[:197] + '...'
			
	return render_to_response('competitions.html', {'competitions': competitions},
							  context_instance=RequestContext(request))

def single(request, competition_id):
	competition = get_object_or_404(Competition, pk=competition_id)
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
    return None
