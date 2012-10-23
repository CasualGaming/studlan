# -*- coding: utf-8 -*-

import uuid

from django.contrib import auth
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect

from studlan import settings
from studlan.authentication.forms import (LoginForm, RegisterForm, 
                            RecoveryForm, ChangePasswordForm)
from studlan.authentication.models import RegisterToken
from studlan.misc.forms import InlineSpanErrorList
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
                    ntnu_username=cleaned['ntnu_username'],
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

Note that tokens have a valid lifetime of 24 hours. If you do not use this
link within 24 hours, it will be invalid, and you will need to use the password
recovery option to get your account verified.
""" % (request.META['HTTP_HOST'], token)

                send_mail('Verify your account', email_message, settings.STUDLAN_FROM_MAIL, [user.email,])

                messages.success(request, 'Registration successful. Check your email for verification instructions.')

                return HttpResponseRedirect('/')        
            else:
                form = RegisterForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
        else:
            form = RegisterForm()

        return render(request, 'auth/register.html', {'form': form, })

def verify(request, token):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        rt = get_object_or_404(RegisterToken, token=token)
        
        if rt.is_valid:
            user = getattr(rt, 'user')

            user.is_active = True
            user.save()
            rt.delete()

            messages.success(request, "User %s successfully activated. You can now log in." % user.username)

            return redirect('auth_login')
        else:
            messages.error(request, "The token has expired. Please use the password recovery to get a new token.")
            return HttpResponseRedirect('/')        
            

def recover(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            form = RecoveryForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                users = User.objects.filter(email=email)

                if len(users) == 0:
                    messages.error(request, "That email is not registered.")
                    return HttpResponseRedirect('/')        

                user = users[0]
                user.save()
    
                # Create the registration token
                token = uuid.uuid4().hex
                rt = RegisterToken(user=user, token=token)
                rt.save()

                email_message = u"""
You have requested a password recovery for the account bound to %s.

Username: %s

If you did not ask for this password recovery, please ignore this email.

Otherwise, click the link below to reset your password;
http://%s/auth/set_password/%s/

Note that tokens have a valid lifetime of 24 hours. If you do not use this
link within 24 hours, it will be invalid, and you will need to use the password
recovery option again to get your account verified.
""" % (email, user.username, request.META['HTTP_HOST'], token)
                

                send_mail('Account recovery', email_message, settings.STUDLAN_FROM_MAIL, [email,])

                messages.success(request, 'A recovery link has been sent to %s.' % email)

                return HttpResponseRedirect('/')        
            else:
                form = RecoveryForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
        else:
            form = RecoveryForm()

        return render(request, 'auth/recover.html', {'form': form})

def set_password(request, token=None): 
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        rt = get_object_or_404(RegisterToken, token=token)
       
        if rt.is_valid:
            if request.method == 'POST':
                form = ChangePasswordForm(request.POST, auto_id=True, error_class=InlineSpanErrorList)
                if form.is_valid():
                    user = getattr(rt, 'user')

                    user.is_active = True
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()
                    
                    rt.delete()

                    messages.success(request, "User %s successfully had it's password changed. You can now log in." % user)
                    
                    return HttpResponseRedirect('/')        
            else:
                
                form = ChangePasswordForm()

                messages.success(request, "Token accepted. Please insert your new password.")

            return render(request, 'auth/set_password.html', {'form': form, 'token': token})

        else:
            messages.error(request, "The token has expired. Please use the password recovery to get a new token.")
            return HttpResponseRedirect('/')        
