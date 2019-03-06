# -*- coding: utf-8 -*-

from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe


class InlineSpanErrorList(ErrorList):
    def __unicode__(self):
        return self.as_spans()

    def as_spans(self):
        if not self:
            return u''
        return mark_safe(''.join([u'<span class="help-inline alert alert-error">{0}</span>'.format(e) for e in self]))  # noqa: S308, S703: Potential XSS
