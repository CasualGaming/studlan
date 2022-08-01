# -*- coding: utf-8 -*-

import datetime
import re

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.userprofile.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nick', 'date_of_birth', 'address', 'zip_code', 'phone', 'marketing_optin')
        widgets = {
            'nick': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _(u'Nickname'), 'type': 'text'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _(u'Street address'), 'type': 'text'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _(u'Postal code'), 'type': 'number'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _(u'Phone number'), 'type': 'tel'}),
            'marketing_optin': forms.CheckboxInput()}

    def clean(self):
        cleaned_data = super(UserProfileForm, self).clean()
        if self.is_valid():

            # Profile check must be consistent with RegisterForm

            # Check nick
            nick = cleaned_data['nick']
            if not re.match('^[a-zA-Z0-9_-]+$', nick):
                self.add_error('nick', ugettext(u'Your desired nickname contains illegal characters. Valid: a-Z 0-9 - _'))

            # Check date of birth
            now = datetime.date.today()
            date = cleaned_data['date_of_birth']
            if date == now:
                self.add_error('date_of_birth', ugettext(u'You seem to have been born today, that doesn\'t seem right.'))
            if date >= now:
                self.add_error('date_of_birth', ugettext(u'You seem to be from the future, that doesn\'t seem right.'))
            if date < now.replace(year=(now.year - 150)):
                self.add_error('date_of_birth', ugettext(u'You seem to be over 150 years old, that doesn\'t seem right.'))

            # ZIP code digits only
            zip_code = cleaned_data['zip_code']
            if len(zip_code) != 4 or not zip_code.isdigit():
                self.add_error('zip_code', ugettext(u'The postal code must be a 4 digit number.'))

            # Phone number digits and plus only
            phone = cleaned_data['phone']
            if not re.match('^((\\+|00)[0-9]{2})?[0-9]{8,10}$', phone):
                self.add_error('phone', ugettext(u'The phone number must consist of an optional country code followed by 8–10 digits (no spaces or symbols, but "+" allowed in country code).'))

            return cleaned_data
