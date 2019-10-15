# -*- coding: utf-8 -*-

import datetime
import re

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.userprofile.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nick', 'date_of_birth', 'address', 'zip_code', 'phone')
        widgets = {
            'nick': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _(u'Nickname'), 'type': 'text'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _(u'Street address'), 'type': 'text'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _(u'Postal code'), 'type': 'number'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _(u'Phone number'), 'type': 'tel'})}

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
        if self.is_valid():

            # Check nick
            nick = cleaned_data['nick']
            if not re.match('^[a-zA-Z0-9_-]+$', nick):
                self.add_error('nick', ugettext(u'Your desired nickname contains illegal characters. Valid: a-Z 0-9 - _'))

            # Check date of birth
            # currently only checks that it is not after today
            date = cleaned_data['date_of_birth']
            if date >= datetime.date.today():
                self.add_error('date_of_birth', ugettext(u'You seem to be from the future, please enter a more believable date of birth.'))

            # ZIP code digits only
            zip_code = cleaned_data['zip_code']
            if len(zip_code) != 4 or not zip_code.isdigit():
                self.add_error('zip_code', ugettext(u'The postal code must be a 4 digit number.'))

            # Phone number digits and plus only
            phone = cleaned_data['phone']
            if not re.match('^((\\+|00)[0-9]{2})?[0-9]{8,10}$', phone):
                self.add_error('phone', ugettext(u'The phone number must consist of an optional country code followed by 8–10 digits (no spaces or symbols, but "+" allowed in country code).'))

            return cleaned_data
