# -*- coding: utf-8 -*-

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.userprofile.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': _('Username'), 'type': 'text'}),
                               label=_('Username'), max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'class': 'form-control',
                                                                                     'placeholder': _('Password'),
                                                                                     'type': 'password'}),
                               label=_('Password'))
    user = None

    def clean(self):
        if self._errors:
            return

        auth_user = auth.authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        if auth_user and auth_user.is_active:
            self.user = auth_user
        else:
            self.add_error('__all__', ugettext('Login failed! Either the account does not exist, it is inactive, or the username–password combination is incorrect.'))
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
    desired_username = forms.CharField(label=_('Desired username'), max_length=20,
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': _('Username'),
                                                  'type': 'text'}))
    first_name = forms.CharField(label=_('First name'), max_length=50,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control', 'placeholder': _('First name'), 'type': 'text'}))
    last_name = forms.CharField(label=_('Last name'), max_length=50,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control', 'placeholder': _('Last name'), 'type': 'text'}))
    date_of_birth = forms.DateField(label=_('Date of birth'),
                                    widget=forms.TextInput(
                                        attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}))
    address = forms.CharField(label=_('Address'), max_length=50,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'placeholder': _('Address'), 'type': 'text'}))
    zip_code = forms.CharField(label=_('Postal code'), max_length=4,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': _('Postal code'), 'type': 'number'}))
    phone = forms.CharField(label=_('Phone number'), max_length=20,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': _('Phone number'), 'type': 'number'}))
    marketing_optin = forms.BooleanField(label=_('Receive emails about upcoming LANs etc. (marketing)'), required=False)
    email = forms.EmailField(label=_('Email address'), max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': _('Email address'), 'type': 'text'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                          attrs={'class': 'form-control', 'placeholder': _('Password'),
                                                                 'type': 'password'}), label=_('Password'))
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                                 attrs={'class': 'form-control',
                                                                        'placeholder': _('Repeat password'),
                                                                        'type': 'password'}),
                                      label=_('Repeat password'))

    def clean(self):
        super(RegisterForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data

            # Check username
            username = cleaned_data['desired_username']
            username_error = UserProfile.check_username(username)
            if username_error:
                self.add_error('desired_username', username_error)

            # Check date of birth
            date_of_birth = cleaned_data['date_of_birth']
            date_of_birth_error = UserProfile.check_date_of_birth(date_of_birth)
            if date_of_birth_error:
                self.add_error('date_of_birth', date_of_birth_error)

            # ZIP code digits only
            zip_code = cleaned_data['zip_code']
            zip_code_error = UserProfile.check_zip_code(zip_code)
            if zip_code_error:
                self.add_error('zip_code', zip_code_error)

            # Phone number digits and plus only
            phone = cleaned_data['phone']
            phone_error = UserProfile.check_phone(phone)
            if phone_error:
                self.add_error('phone', phone_error)

            # Check passwords match
            if cleaned_data['password'] != cleaned_data['repeat_password']:
                self.add_error('repeat_password', [ugettext('Passwords did not match.')])

            # Check passwords strength
            if len(cleaned_data['password']) < 8:
                self.add_error('password', [ugettext('Password must be at least 8 characters long.')])

            return cleaned_data


class RecoveryForm(forms.Form):
    email = forms.EmailField(label=_('Email'), max_length=50,
                             widget=forms.EmailInput(
                                 attrs={'class': 'form-control', 'placeholder': _('Email'), 'type': 'text'}))


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                              attrs={'class': 'form-control',
                                                                     'placeholder': _('Password'),
                                                                     'type': 'password'}), label=_('New password'))
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False,
                                                                 attrs={'class': 'form-control',
                                                                        'placeholder': _('Repeat password'),
                                                                        'type': 'password'}), label=_('Repeat new password'))

    def clean(self):
        super(ChangePasswordForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data

            # Check passwords match
            if cleaned_data['new_password'] != cleaned_data['repeat_password']:
                self._errors['repeat_password'] = self.error_class(ugettext('Passwords did not match.'))

            # Check passwords strength
            if len(cleaned_data['new_password']) < 8:
                self.add_error('new_password', [ugettext('Password must be at least 8 characters long.')])

            return cleaned_data
