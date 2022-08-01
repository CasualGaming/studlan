# -*- coding: utf-8 -*-

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

            # Check nick
            nick = cleaned_data['nick']
            nick_error = UserProfile.check_nick(nick)
            if nick_error:
                self.add_error('nick', nick_error)

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

            return cleaned_data
