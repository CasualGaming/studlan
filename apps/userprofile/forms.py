# -*- coding: utf-8 -*-

import datetime
import re

from django import forms
from django.utils.translation import ugettext as _

from apps.userprofile.models import UserProfile

class UserProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('nick', 'gender', 'date_of_birth', 'address', 'zip_code', 'phone',)
		widgets = {
            'nick': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nickname', 'type': 'text'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address', 'type': 'text'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'zip code', 'type': 'number'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number', 'type': 'number'})}

	def clean(self):
	    super(UserProfileForm, self).clean()
	    if self.is_valid():
	        cleaned_data = self.cleaned_data

	        # Check nick
            nick = cleaned_data['nick']
            if not re.match("^[a-zA-Z0-9_-]+$", nick):
                self._errors['nick'] = self.error_class([_(u"Your desired nickname contains illegal characters. Valid: a-Z 0-9 - _")])
	        
	        # Check date of birth
	        # currently only checks that it is not after today
	        date = cleaned_data['date_of_birth']
	        if date >= datetime.date.today():
	            self._errors['date_of_birth'] = self.error_class([_(u"You seem to be from the future, please enter a more believable date of birth.")])

	        # ZIP code digits only
	        zip_code = cleaned_data['zip_code']
	        if len(zip_code) != 4 or not zip_code.isdigit():
	            self._errors['zip_code'] = self.error_class([_(u"The ZIP code must be 4 digit number.")])

	        return cleaned_data 

