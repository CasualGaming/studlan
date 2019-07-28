# -*- coding: utf-8 -*-

import re

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

from apps.team.models import Team


class TeamCreationForm(forms.Form):
    title = forms.CharField(label=_(u'Title'), max_length=30)
    tag = forms.CharField(label=_(u'Tag'), max_length=10)

    def clean(self):
        super(TeamCreationForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data

            # Validate the tag
            tag = cleaned_data['tag']
            if not re.match('^[a-zA-Z0-9_-]+$', tag):
                self.add_error('tag', ugettext(u'Your desired tag contains illegal characters. Valid: a-Z 0-9 - _'))

            if Team.objects.filter(tag=tag).exists():
                self.add_error('tag', ugettext(u'This team tag is already taken.'))

            return cleaned_data
