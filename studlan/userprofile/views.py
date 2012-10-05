# -*- coding: utf-8 -*-

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from studlan.lan.models import Attendee, LAN
from studlan.userprofile.forms import UserProfileForm
from studlan.userprofile.models import UserProfile

@login_required
def my_profile(request):
    profile = request.user.get_profile()

    return render(request, 'user/profile.html', {'quser': request.user, 'profile': profile})

def update_profile(request):
    if request.method == 'GET':
        form = UserProfileForm(instance=request.user.get_profile(), auto_id=True)
    else:
        form = UserProfileForm(request.POST, instance=request.user.get_profile(), auto_id=True)
        if form.is_valid():
            form.save()
            return redirect('myprofile')

    return render(request, 'user/update.html', {'form': form})

def user_profile(request, username):
    # Using quser for "queried user", as "user" is a reserved variable name in templates
    quser = get_object_or_404(User, username=username)

    # If the user is authenticated and are doing a lookup on themselves, also create
    # the form for updating and showing update information.
    if request.user.is_authenticated() and request.user == quser:
        return my_profile(request)

    profile = quser.get_profile()
    
    return render(request, 'user/profile.html', {'quser': quser, 'profile': profile})

def history(request):
    attended = Attendee.objects.filter(user=request.user)

    return render(request, 'user/history.html', {'attended': attended})
