# -*- coding: utf-8 -*-

from django import forms
from django.forms.util import ErrorList
from django.utils.safestring import mark_safe

from studlan.userprofile.models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nick', 'signed_up', 'wants_to_sit_with', 'gender', 'date_of_birth', 'address', 'zip_code', 'phone',)

class InlineSpanErrorList(ErrorList):
    def __unicode__(self):
        return self.as_spans()
    def as_spans(self):
        if not self: return u''
        return mark_safe(''.join([u'<span class="help-inline alert alert-error">%s</span>' % e for e in self]))
