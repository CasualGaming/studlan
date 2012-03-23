# -*- coding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from studlan.auth.forms import LoginForm, RegisterForm
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
                
                user = User(
                    username=cleaned['desired_username'], 
                    first_name=cleaned['first_name'], 
                    last_name=cleaned['last_name'],
                )
                user.set_password(cleaned['password'])
                user.save()

                
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
                
                messages.success(request, 'Registration successful. You may now log in.')

                return redirect('auth_login')        
        else:
            form = RegisterForm()

        return render(request, 'auth/register.html', {'form': form, })
