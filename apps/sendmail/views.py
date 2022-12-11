# -*- coding: utf-8 -*-

import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_safe

from apps.misc.forms import InlineSpanErrorList
from apps.userprofile.models import User

from .forms import SendMessageForm
from .models import Mail, MailRecipient


sendmail_logger = logging.getLogger('sendmail')


@require_safe
@login_required
@permission_required('sendmail.list')
def sendmail_list(request):
    mails = Mail.objects.order_by('-created_time')[:50]
    mail_count = mails.count()
    mail_total_count = Mail.objects.count()
    return render(request, 'sendmail/list.html', {'mails': mails, 'mail_count': mail_count, 'mail_total_count': mail_total_count})


@require_safe
@login_required
@permission_required('sendmail.view')
def sendmail_view(request, mail_uuid):
    mail = get_object_or_404(Mail, pk=mail_uuid)
    return render(request, 'sendmail/view.html', {'mail': mail})


@login_required
@permission_required('sendmail.send')
def sendmail_send(request):
    template_context = {}
    form = SendMessageForm()

    if request.method == 'POST':
        # Validate and send if ok, otherwise return it again
        current_form = SendMessageForm(request.POST, error_class=InlineSpanErrorList)
        form = handle_send_form(request, current_form, template_context)
        if form is None:
            return redirect('sendmail_list')

    template_context['form'] = form
    return render(request, 'sendmail/send.html', template_context)


def handle_send_form(request, form, template_context):
    if not form.is_valid():
        return form

    fields = form.cleaned_data
    mail_uuid = fields['mail_uuid']
    mail_language = fields['language']
    mail_subject = fields['subject']
    mail_content = fields['content']

    # Reject duplicate message
    if Mail.objects.filter(uuid=mail_uuid).exists():
        messages.error(request, _('The mail has already been sent. If this is a new message, please reload the page and try again.'))
        return form

    # Build recipient list
    recipient_users = build_recipient_list(request, fields)
    recipients_count = len(recipient_users)

    # If "send" wasn't pressed, show existing form but with preview
    if 'send' not in form.data:
        template_context['mail_subject'] = mail_subject
        template_context['mail_content'] = mail_content
        template_context['mail_recipient_count'] = recipients_count
        return form

    # Send mail
    with transaction.atomic():
        # Create mail
        mail = Mail()
        mail.uuid = mail_uuid
        mail.language = mail_language
        mail.sender = request.user
        mail.subject = mail_subject
        mail.content = mail_content
        mail.save()

        # Create recipients
        for user in recipient_users:
            recipient = MailRecipient()
            recipient.mail = mail
            recipient.user = user
            recipient.save()

        sendmail_logger.info('Prepared mail "%s" with %d recipients.', mail.uuid, recipients_count)

    # Show new form
    messages.success(request, _('Successfully created the message with {user_count} recipient(s).').format(user_count=recipients_count))
    return None


def build_recipient_list(request, fields):
    all_recipients = User.objects.none()

    # Everyone (marketing)
    everyone = fields['recipient_everyone_marketing']
    if everyone:
        all_recipients = User.objects.filter(profile__marketing_optin=True)

    # Everyone
    everyone = fields['recipient_everyone']
    if everyone:
        all_recipients = User.objects.all()

    # LAN attendees
    lan_attendees = fields['recipient_lan_attendees']
    lan_attendee_users = User.objects.filter(attendee__lan__in=lan_attendees)
    all_recipients = all_recipients.union(lan_attendee_users)

    # LAN payers
    lan_payers = fields['recipient_lan_payers']
    lan_payer_users = User.objects.filter(
        (Q(attendee__lan__in=lan_payers) & Q(attendee__has_paid=True))
        | Q(ticket__ticket_type__lan__in=lan_payers),
    )
    all_recipients = all_recipients.union(lan_payer_users)

    # Tickets
    tickets = fields['recipient_tickets']
    ticket_users = User.objects.filter(ticket__ticket_type__in=tickets)
    all_recipients = all_recipients.union(ticket_users)

    # Teams
    teams = fields['recipient_teams']
    team_users = User.objects.filter(Q(newteamleader__in=teams) | Q(new_team_members__in=teams))
    all_recipients = all_recipients.union(team_users)

    # Competitions
    competitions = fields['recipient_competitions']
    competition_users = User.objects.filter(
        Q(newteamleader__participant__competition__in=competitions)
        | Q(new_team_members__participant__competition__in=competitions)
        | Q(participant__competition__in=competitions),
    )
    all_recipients = all_recipients.union(competition_users)

    # Specific users
    specific_users = fields['recipient_users']
    all_recipients = all_recipients.union(specific_users)

    # Yourself
    yourself = fields['recipient_yourself']
    if yourself:
        all_recipients = all_recipients.union(User.objects.filter(id=request.user.id))

    # Resolve queryset and get rid of duplicates (which appear for some reason)
    all_recipients_set = set(all_recipients)

    return all_recipients_set
