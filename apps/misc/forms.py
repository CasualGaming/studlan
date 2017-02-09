# -*- coding: utf-8 -*-

from django.utils.safestring import mark_safe

class InlineSpanErrorList():
    def __unicode__(self):
        return self.as_spans()
    def as_spans(self):
        if not self: return u''
        return mark_safe(''.join([u'<span class="help-inline alert alert-error">%s</span>' % e for e in self]))
