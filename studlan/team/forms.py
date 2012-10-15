# -*- coding: utf-8 -*-

import re

from django import forms

class TeamCreationForm(forms.Form):
    title = forms.CharField(label="Title", max_length=50)
    tag = forms.CharField(label="Tag", max_length=10)

    def clean(self):
        super(TeamCreationForm, self).clean()
        if self.is_valid():
            cleaned_data = self.cleaned_data  


            # Validate the tag
            tag = cleaned_data['tag']
            if not re.match("^[a-zA-Z0-9_-]+$", tag):
                self._errors['tag'] = self.error_class(["Your desired tag contains illegal characters. Valid: a-Z 0-9 - _"])

            return cleaned_data
