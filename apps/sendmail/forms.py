# -*- coding: utf-8 -*-

import uuid

from django import forms
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.text import format_lazy
from django.utils.translation import ugettext_lazy as _

from apps.competition.models import Competition
from apps.lan.models import LAN, TicketType
from apps.team.models import Team
from apps.userprofile.models import User


class SendMessageForm(forms.Form):
    _select_multiple_help = _(u'Select zero, one or multiple by control-clicking.')
    _select_multiple_size = '5'

    language = forms.ChoiceField(
        label=_(u'Language'),
        required=True,
        choices=settings.LANGUAGES)
    mail_uuid = forms.UUIDField(
        required=True,
        initial=uuid.uuid4,
        widget=forms.HiddenInput())
    subject = forms.CharField(
        label=_(u'Subject'),
        required=True,
        max_length=100)
    content = forms.CharField(
        label=_(u'Content'),
        required=True,
        strip=True,
        help_text=_(u'Markdown formatting is supported. The message will be sent as both HTML and plaintext, so make sure to add important links as plaintext.'),
        widget=forms.Textarea)
    recipient_everyone_marketing = forms.BooleanField(
        label=_(u'All users (marketing)'),
        required=False,
        help_text=_(u'Send to users which have opted in to marketing emails.'))
    recipient_everyone = forms.BooleanField(
        label=_(u'All users'),
        required=False,
        help_text=_(u'Send to all users. Never use for marketing purposes!'))
    recipient_lan_attendees = forms.ModelMultipleChoiceField(
        label=_(u'LAN attendees'),
        queryset=LAN.objects.all(),
        required=False,
        help_text=format_lazy(u'{0} {1}', _(u'Users which pressed "attend". Appropriate for public LAN updates.'), _select_multiple_help),
        widget=forms.SelectMultiple(attrs={'size': _select_multiple_size}))
    recipient_lan_payers = forms.ModelMultipleChoiceField(
        label=_(u'LAN payers'),
        queryset=LAN.objects.all(),
        required=False,
        help_text=format_lazy(u'{0} {1}', _(u'Users which paid by the door (i.e. no ticket) (if allowed for the LAN). Appropriate for LAN updates.'), _select_multiple_help),
        widget=forms.SelectMultiple(attrs={'size': _select_multiple_size}))
    recipient_tickets = forms.ModelMultipleChoiceField(
        label=_(u'Ticket owners'),
        queryset=TicketType.objects.all(),
        required=False,
        help_text=format_lazy(u'{0} {1}', _(u'Users which bought/received a ticket for the LAN. Appropriate for LAN updates.'), _select_multiple_help),
        widget=forms.SelectMultiple(attrs={'size': _select_multiple_size}))
    recipient_teams = forms.ModelMultipleChoiceField(
        label=_(u'Teams'),
        queryset=Team.objects.all(),
        required=False,
        help_text=_select_multiple_help,
        widget=forms.SelectMultiple(attrs={'size': _select_multiple_size}))
    recipient_competitions = forms.ModelMultipleChoiceField(
        label=_(u'Competitions'),
        queryset=Competition.objects.all(),
        required=False,
        help_text=_select_multiple_help,
        widget=forms.SelectMultiple(attrs={'size': _select_multiple_size}))
    recipient_users = forms.CharField(
        label=_(u'Individual users'),
        required=False,
        help_text=_(u'Specify usernames separated by comma. Case sensitive.'))
    recipient_yourself = forms.BooleanField(
        label=_(u'Yourself'),
        required=False,
        help_text=_(u'Send to yourself.'))

    def clean(self):
        cleaned_data = super(SendMessageForm, self).clean()

        # At least one recipient
        if not (
            cleaned_data.get('recipient_everyone_marketing')
            or cleaned_data.get('recipient_everyone')
            or cleaned_data.get('recipient_yourself')
            or cleaned_data.get('recipient_lan_attendees')
            or cleaned_data.get('recipient_lan_payers')
            or cleaned_data.get('recipient_tickets')
            or cleaned_data.get('recipient_teams')
            or cleaned_data.get('recipient_competitions')
            or cleaned_data.get('recipient_users')
        ):
            self.add_error(None, _(u'At least one recipient is required.'))

        # Parse users string
        users_raw = cleaned_data.get('recipient_users')
        users_raw = users_raw.replace(u' ', u'')
        users_raw = users_raw.split(u',')
        found_users_qs = User.objects.none()
        missing_users_string = u''
        for username in users_raw:
            user_qs = User.objects.filter(username=username)
            if user_qs:
                found_users_qs = found_users_qs | user_qs
            elif missing_users_string == u'':
                missing_users_string = username
            else:
                missing_users_string = u'{0}, {1}'.format(missing_users_string, username)
        if missing_users_string:
            self.add_error(None, _(u'Users not found: {users}').format(users=missing_users_string))
        cleaned_data['recipient_users'] = found_users_qs

        # Clean content
        cleaned_data['content'] = strip_tags(cleaned_data.get('content'))
