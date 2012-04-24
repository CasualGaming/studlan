# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from studlan.userprofile.forms import UserProfileForm, InlineSpanErrorList
from studlan.userprofile.models import UserProfile

@login_required
def my_profile(request):
    user = request.user
    if request.method == 'GET':
        form = UserProfileForm(instance=request.user.get_profile(), auto_id=True, error_class=InlineSpanErrorList)
    else:
        form = UserProfileForm(request.POST, instance=request.user.get_profile(), auto_id=True, error_class=InlineSpanErrorList)
        if form.is_valid():
            form.save()
    
    profile = user.get_profile()

    return render(request, 'user/profile.html', {'quser': request.user, 'profile': profile, 'form': form})

def user_profile(request, username):
    # Using quser for "queried user", as "user" is a reserved variable name in templates
    quser = get_object_or_404(User, username=username)

    # If the user is authenticated and are doing a lookup on themselves, also create
    # the form for updating and showing update information.
    if request.user.is_authenticated() and request.user == quser:
        return my_profile(request)

    profile = quser.get_profile()
    
    return render(request, 'user/profile.html', {'quser': quser, 'profile': profile})
