# -*- coding: utf-8 -*-

import datetime
import re

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _


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

        auth_user = auth.authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if auth_user and auth_user.is_active:
            self.user = auth_user
        else:
            self.add_error('__all__', ugettext(u'Login failed! Either the account does not exist, it is inactive, or the username–password combination is incorrect.'))
        return self.cleaned_data

    def login(self, request):
        try:
            User.objects.get(username=request.POST['username'])
        except Exception:  # noqa: B902: Blind Exception
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
    email = forms.EmailField(label=_(u'Email address'), max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': _(u'Email address'), 'type': 'text'}))
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
    zip_code = forms.CharField(label=_(u'Postal code'), max_length=4,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': _(u'Postal code'), 'type': 'number'}))
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
                               ugettext(u'You seem to be from the future, please enter a more believable date of birth.'))

            # Check passwords match
            if cleaned_data['password'] != cleaned_data['repeat_password']:
                self.add_error('repeat_password', [ugettext(u'Passwords did not match.')])

            # Check passwords strength
            if len(cleaned_data['password']) < 8:
                self.add_error('password', [ugettext(u'Password must be at least 8 characters long.')])

            # Check username
            username = cleaned_data['desired_username']
            if User.objects.filter(username=username).count() > 0:
                self.add_error('desired_username', ugettext(u'There is already a user with that username.'))
            if not re.match('^[a-zA-Z0-9_-]+$', username):
                self.add_error('desired_username',
                               ugettext(u'Your desired username contains illegal characters. Valid: a-Z 0-9 - _'))

            # ZIP code digits only
            zip_code = cleaned_data['zip_code']
            if len(zip_code) != 4 or not zip_code.isdigit():
                self.add_error('zip_code', ugettext(u'The postal code must be a 4 digit number.'))

            return cleaned_data


class RecoveryForm(forms.Form):
    email = forms.EmailField(label=_(u'Email'), max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': _(u'Email'), 'type': 'text'}))


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                              attrs={'class': 'form-control',
                                                                     'placeholder': _(u'Password'),
                                                                     'type': 'password'}), label=_(u'New password'))
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                                 attrs={'class': 'form-control',
                                                                        'placeholder': _(u'Repeat password'),
                                                                        'type': 'password'}), label=_(u'Repeat new password'))

    def clean(self):
        super(ChangePasswordForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data

            # Check passwords match
            if cleaned_data['new_password'] != cleaned_data['repeat_password']:
                self._errors['repeat_password'] = self.error_class(ugettext(u'Passwords did not match.'))

            # Check passwords strength
            if len(cleaned_data['new_password']) < 8:
                self.add_error('new_password', [ugettext(u'Password must be at least 8 characters long.')])

            return cleaned_data
