# -*- coding: utf-8 -*-

import uuid

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from studlan.authentication.forms import LoginForm, RegisterForm, DivErrorList, InlineSpanErrorList
from studlan.authentication.models import RegisterToken
from studlan.userprofile.models import UserProfile

def login(request):
    redirect_url = request.REQUEST.get('next', '')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.login(request):
            messages.success(request, 'You have successfully logged in.')
            if redirect_url:
                return HttpResponseRedirect(redirect_url)
            return HttpResponseRedirect('/')
        else: form = LoginForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
    else:
        form = LoginForm()

    response_dict = { 'form' : form, 'next' : redirect_url}
    return render(request, 'auth/login.html', response_dict)

def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect('/')

def register(request):
    if request.user.is_authenticated():
        messages.error(request, 'You cannot be logged in when registering.')
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                cleaned = form.cleaned_data
                
                # Create user
                user = User(
                    username=cleaned['desired_username'], 
                    first_name=cleaned['first_name'], 
                    last_name=cleaned['last_name'],
                    email=cleaned['email'],
                )
                user.set_password(cleaned['password'])
                user.is_active = False
                user.save()

                # Create userprofile
                up = UserProfile(
                    user=user, 
                    nick=cleaned['desired_username'],
                    date_of_birth=cleaned['date_of_birth'],
                    gender=cleaned['gender'],
                    zip_code=cleaned['zip_code'],
                    address=cleaned['address'],
                    phone=cleaned['phone'],
                )
                up.save() 

                # Create the registration token
                token = uuid.uuid4().hex
                rt = RegisterToken(user=user, token=token)
                rt.save()

                email_message = u"""
You have registered an account at studlan.no.

To use the account you need to verify it. You can do this by visiting the link below.

http://%s/auth/verify/%s/

""" % (request.META['HTTP_HOST'], token)

                send_mail('Verify your account', email_message, 'studlan@online.ntnu.no', [user.email,])

                messages.success(request, 'Registration successful. Check your email for verification instructions.')

                return HttpResponseRedirect('/')        
            else:
                form = RegisterForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
        else:
            form = RegisterForm()

        return render(request, 'auth/register.html', {'form': form, })

def verify(request, token):
    rt = get_object_or_404(RegisterToken, token=token)

    user = getattr(rt, 'user')

    user.is_active = True
    user.save()

    messages.success(request, "User %s successfully activated. You can now log in." % (user.username))

    return redirect('auth_login')
