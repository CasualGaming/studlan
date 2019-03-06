# -*- coding: utf-8 -*-

import re

from django import forms
from django.utils.translation import ugettext as _

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
                self.add_error('tag', _(u'Your desired tag contains illegal characters. Valid: a-Z 0-9 - _'))

            team = Team.objects.filter(tag=tag)
            if team.count() > 0:
                self.add_error('tag', _(u'This team tag is taken. The team belongs to ') + unicode(team[0].leader))

            return cleaned_data
