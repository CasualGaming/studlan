# -*- coding: utf-8 -*-

from django import forms

from studlan.userprofile.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nick', 'signed_up', 'wants_to_sit_with', 'gender', 'date_of_birth', 'address', 'zip_code', 'phone',)
