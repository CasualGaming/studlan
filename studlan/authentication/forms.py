# -*- coding: utf-8 -*-

import datetime

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

from studlan.userprofile.models import GENDERS

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label="Username", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Password")
    user = None

    def clean(self):
        if self._errors:
            return
    
        user = auth.authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])

        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError("Your account is inactive, contact xxx@xxx.xxx")
        else:
            raise forms.ValidationError("Your account does not exist or the user/password combination is incorrect. Did you remember to register?")
        return self.cleaned_data

    def login(self, request):
        try:
            User.objects.get(username=request.POST['username'])
        except:
            return False
        if self.is_valid():
            auth.login(request, self.user)
            request.session.set_expiry(0)
            return True
        return False

class RegisterForm(forms.Form):
    desired_username = forms.CharField(label="Desired username", max_length=20)
    first_name = forms.CharField(label="First name", max_length=50)
    last_name = forms.CharField(label="Last name", max_length=50)
    date_of_birth = forms.DateField(label="Date of birth", initial=datetime.date.today)
    # Implement in django 1.4. Template contains printing workaround for radiobuttons
    #gender = forms.ChoiceField(label="Gender", widget=RadioSelect, choices=GENDERS)
    gender = forms.ChoiceField(label="Gender", choices=GENDERS)
    email = forms.EmailField(label="Email", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Password")
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Repeat password")
    address = forms.CharField(label="Address", max_length=50)
    zip_code = forms.CharField(label="ZIP code", max_length=4)
    phone = forms.CharField(label="Phone number", max_length=20)
    
    def clean(self):
        super(RegisterForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data
            
            # Check date of birth
            # currently only checks that it is not after today
            date = cleaned_data['date_of_birth']
            if date >= datetime.date.today():
                raise forms.ValidationError("You seem to be from the future, please enter a more believable date of birth.")

            # Check passwords
            if cleaned_data['password'] != cleaned_data['repeat_password']:
                raise forms.ValidationError("Your password do not match.")

            # Check username
            username = cleaned_data['desired_username']
            if User.objects.filter(username=username).count() > 0:
                raise forms.ValidationError("There is already a user with that username.")    

            # Check email
            email = cleaned_data['email']
            if User.objects.filter(email=email).count() > 0:
                raise forms.ValidationError("There is already a user with that email.")    

            # ZIP code digits only
            zip_code = cleaned_data['zip_code']
            if len(zip_code) != 4 or not zip_code.isdigit():
                raise forms.ValidationError("The ZIP code must be 4 digit number.")

            return cleaned_data 
