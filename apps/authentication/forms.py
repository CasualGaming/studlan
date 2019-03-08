# -*- coding: utf-8 -*-

import datetime
import re

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': _(u'Username'), 'type': 'text'}),
                               label=_(u'Username'), max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class': 'form-control',
                                                                                     'placeholder': _(u'Password'),
                                                                                     'type': 'password'}),
                               label=_(u'Password'))
    user = None

    def clean(self):
        if self._errors:
            return

        user = auth.authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])

        if user:
            # Inactive users are not authenticated by the default backend, so all users returned from auth.authenticate are active.
            # But keep this here in case the backend is changed.
            if user.is_active:
                self.user = user
            else:
                self.add_error('username', _(u'Your account is inactive, try to recover it.'))
        else:
            self.add_error('password', _(u'Login failed!'
                                         u' Either the account does not exist, is inactive, or the username–password combination is incorrect.'
                                         u' If you believe the account exists or you have forgotten the username or password, try the password recovery feature.'))
        return self.cleaned_data

    def login(self, request):
        try:
            User.objects.get(username=request.POST['username'])
        except Exception:
            return False
        if self.is_valid():
            auth.login(request, self.user)
            request.session.set_expiry(0)
            return True
        return False


class RegisterForm(forms.Form):
    desired_username = forms.CharField(label=_(u'Desired username'), max_length=20,
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': _(u'Username'),
                                                  'type': 'text'}))
    first_name = forms.CharField(label=_(u'First name'), max_length=50,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': _(u'First name'), 'type': 'text'}))
    last_name = forms.CharField(label=_(u'Last name'), max_length=50,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': _(u'Last name'), 'type': 'text'}))
    date_of_birth = forms.DateField(label=_(u'Date of birth'),
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control', 'placeholder': u'YYYY-MM-DD', 'type': 'date'}))
    email = forms.EmailField(label=_(u'Email'), max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': _(u'Email'), 'type': 'text'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                          attrs={'class': 'form-control', 'placeholder': _(u'Password'),
                                                                 'type': 'password'}), label=_(u'Password'))
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                                 attrs={'class': 'form-control',
                                                                        'placeholder': _(u'Repeat password'),
                                                                        'type': 'password'}),
                                      label=_(u'Repeat password'))
    address = forms.CharField(label=_(u'Address'), max_length=50,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': _(u'Address'), 'type': 'text'}))
    zip_code = forms.CharField(label=_(u'ZIP code'), max_length=4,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': _(u'Zip code'), 'type': 'number'}))
    phone = forms.CharField(label=_(u'Phone number'), max_length=20,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': _(u'Phone number'), 'type': 'number'}))

    def clean(self):
        super(RegisterForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data

            # Check date of birth
            # currently only checks that it is not after today
            date = cleaned_data['date_of_birth']
            if date >= datetime.date.today():
                self.add_error('date_of_birth',
                               _(u'You seem to be from the future, please enter a more believable date of birth.'))

            # Check passwords
            if cleaned_data['password'] != cleaned_data['repeat_password']:
                self.add_error('repeat_password', [_(u'Passwords did not match.')])

            # Check username
            username = cleaned_data['desired_username']
            if User.objects.filter(username=username).count() > 0:
                self.add_error('desired_username', _(u'There is already a user with that username.'))
            if not re.match('^[a-zA-Z0-9_-]+$', username):
                self.add_error('desired_username',
                               _(u'Your desired username contains illegal characters. Valid: a-Z 0-9 - _'))

            # Check email
            email = cleaned_data['email']
            if User.objects.filter(email=email).count() > 0:
                self.add_error('email', _(u'There is already a user with that email.'))

            # ZIP code digits only
            zip_code = cleaned_data['zip_code']
            if len(zip_code) != 4 or not zip_code.isdigit():
                self.add_error('zip_code', _(u'The ZIP code must be 4 digit number.'))

            return cleaned_data


class RecoveryForm(forms.Form):
    email = forms.EmailField(label=_(u'Email'), max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': _(u'Email'), 'type': 'text'}))


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_(u'New password'))
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label=_(u'Repeat new password'))

    def clean(self):
        super(ChangePasswordForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data

            # Check passwords
            if cleaned_data['new_password'] != cleaned_data['repeat_password']:
                self._errors['repeat_password'] = self.error_class(_(u'Passwords did not match.'))

            return cleaned_data
