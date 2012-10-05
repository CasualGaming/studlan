# -*- coding: utf-8 -*-

import datetime

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe

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
                self._errors['username'] = self.error_class(["Your account is inactive, try to recover it."])
        else:
            self._errors['username'] = self.error_class(["The account does not exist, or username/password combination is incorrect."])
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
                self._errors['date_of_birth'] = self.error_class(["You seem to be from the future, please enter a more believable date of birth."])

            # Check passwords
            if cleaned_data['password'] != cleaned_data['repeat_password']:
                self._errors['repeat_password'] = self.error_class(["Passwords did not match."])

            # Check username
            username = cleaned_data['desired_username']
            if User.objects.filter(username=username).count() > 0:
                self._errors['desired_username'] = self.error_class(["There is already a user with that username."])

            # Check email
            email = cleaned_data['email']
            if User.objects.filter(email=email).count() > 0:
                self._errors['email'] = self.error_class(["There is already a user with that email."])

            # ZIP code digits only
            zip_code = cleaned_data['zip_code']
            if len(zip_code) != 4 or not zip_code.isdigit():
                self._errors['zip_code'] = self.error_class(["The ZIP code must be 4 digit number."])

            return cleaned_data 

class RecoveryForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50)

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Old password", required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="New password")
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label="Repeat new password")

    def clean(self):
        super(ChangePasswordForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data

            # Check passwords
            if cleaned_data['new_password'] != cleaned_data['repeat_password']:
                self._errors['repeat_password'] = self.error_class(["Passwords did not match."])

            return cleaned_data

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return mark_safe(u'<div class="errorlist">%s</div>' % ''.join([u'<div class="alert-message block-message error">%s</div>' % e for e in self]))

class InlineSpanErrorList(ErrorList):
    def __unicode__(self):
        return self.as_spans()
    def as_spans(self):
        if not self: return u''
        return mark_safe(''.join([u'<span class="help-inline alert alert-error">%s</span>' % e for e in self]))
