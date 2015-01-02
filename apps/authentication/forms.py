# -*- coding: utf-8 -*-

import datetime
import re

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from apps.misc.forms import InlineSpanErrorList
from apps.userprofile.models import GENDERS

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _(u'Username'), 'type': 'text'}), label="Username", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class':'form-control', 'placeholder': _(u'Password'), 'type': 'password'}), label="Password")
    user = None

    def clean(self):
        if self._errors:
            return
    
        user = auth.authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])

        if user:
            if user.is_active:
                self.user = user
            else:
                self._errors['username'] = self.error_class([_(u"Your account is inactive, try to recover it.")])
        else:
            self._errors['username'] = self.error_class([_(u"The account does not exist, or username/password combination is incorrect.")])
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
    desired_username = forms.CharField(label=_(u"Desired username"), max_length=20, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _(u'Username'), 'type': 'text'}))
    ntnu_username = forms.CharField(label=_(u"NTNU username"), max_length=20, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _(u'NTNU user'), 'type': 'text'    }))
    first_name = forms.CharField(label=_(u"First name"), max_length=50, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _(u'First name'), 'type': 'text'})) 
    last_name = forms.CharField(label=_(u"Last name"), max_length=50, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _(u'Last name'), 'type': 'text'}))
    date_of_birth = forms.DateField(label=_(u"Date of birth"), initial=datetime.date.today, 
        widget=forms.DateInput(attrs={'class':'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(label=_(u"Gender"), choices=GENDERS, 
        widget=forms.Select(attrs={'class':'form-control'}))
    email = forms.EmailField(label=_(u"Email"), max_length=50, 
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': _(u'Email'), 'type': 'text'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, 
        attrs={'class':'form-control', 'placeholder': _(u'Password'), 'type': 'password'}), label=_(u"Password"))
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False,    
        attrs={'class':'form-control', 'placeholder': _(u'Repeat password'), 'type': 'password'}), label=_(u"Repeat password"))
    address = forms.CharField(label=_(u"Address"), max_length=50, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _(u'Address'), 'type': 'text'}))
    zip_code = forms.CharField(label=_(u"ZIP code"), max_length=4, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _(u'Zip code'), 'type': 'number'}))
    phone = forms.CharField(label=_(u"Phone number"), max_length=20, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': _(u'Phone number'), 'type': 'number'}))
    
    def clean(self):
        super(RegisterForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data
            
            # Check date of birth
            # currently only checks that it is not after today
            date = cleaned_data['date_of_birth']
            if date >= datetime.date.today():
                self._errors['date_of_birth'] = self.error_class([_(u"You seem to be from the future, please enter a more believable date of birth.")])

            # Check passwords
            if cleaned_data['password'] != cleaned_data['repeat_password']:
                self._errors['repeat_password'] = self.error_class([_(u"Passwords did not match.")])

            # Check username
            username = cleaned_data['desired_username']
            if User.objects.filter(username=username).count() > 0:
                self._errors['desired_username'] = self.error_class([_(u"There is already a user with that username.")])
            if not re.match("^[a-zA-Z0-9_-]+$", username):
                self._errors['desired_username'] = self.error_class([_(u"Your desired username contains illegal characters. Valid: a-Z 0-9 - _")])

            # Check email
            email = cleaned_data['email']
            if User.objects.filter(email=email).count() > 0:
                self._errors['email'] = self.error_class([_(u"There is already a user with that email.")])

            # ZIP code digits only
            zip_code = cleaned_data['zip_code']
            if len(zip_code) != 4 or not zip_code.isdigit():
                self._errors['zip_code'] = self.error_class([_(u"The ZIP code must be 4 digit number.")])

            return cleaned_data 

class RecoveryForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50)

class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_(u"New password"))
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_(u"Repeat new password"))

    def clean(self):
        super(ChangePasswordForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data

            # Check passwords
            if cleaned_data['new_password'] != cleaned_data['repeat_password']:
                self._errors['repeat_password'] = self.error_class([_(u"Passwords did not match.")])

            return cleaned_data
