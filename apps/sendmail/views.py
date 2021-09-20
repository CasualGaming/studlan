# -*- coding: utf-8 -*-

from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core import mail as django_mail
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

from apps.misc.forms import InlineSpanErrorList
from apps.userprofile.models import User

from .forms import SendMessageForm
from .models import Mail


@login_required
@permission_required('sendmail.send_mail')
def sendmail_send(request):
    template_context = {}

    if request.method == 'POST':
        old_form = SendMessageForm(request.POST, error_class=InlineSpanErrorList)
        form = handle_submitted_form(request, old_form, template_context)
    else:
        form = SendMessageForm()

    if Mail.objects.filter(done_sending=False).exists():
        messages.warning(request, _(u'There are currently mails that are being sent. Please wait before sending a new mail. '
                                    u'If you believe this is incorrect, please check the admin panel and delete any old, unfinished mails.'))
    else:
        messages.info(request, _(u'There are currently no mails that are being sent.'))

    template_context['form'] = form
    return render(request, 'sendmail/send.html', template_context)


def handle_submitted_form(request, old_form, template_context):
    if not old_form.is_valid():
        return old_form

    fields = old_form.cleaned_data

    form_id = fields['form_id']
    if Mail.objects.filter(form_id=form_id).exists():
        # Reject duplicate message
        messages.error(request, _(u'The mail has already been sent. If this is a new message, please reload the page and try again.'))
        return old_form

    subject = fields['subject']
    content = fields['content']

    # Build recipient list
    everyone = fields['everyone']
    if everyone:
        all_recipients = User.objects.all()
    else:
        all_recipients = User.objects.none()

        yourself = fields['yourself']
        if yourself:
            all_recipients = all_recipients.union(request.user)

        lan_attendees = fields['lan_attendees']
        lan_attendee_users = User.objects.filter(attendee__lan__in=lan_attendees)
        all_recipients = all_recipients.union(lan_attendee_users)

        lan_payers = fields['lan_payers']
        lan_payer_users = User.objects.filter(
            (Q(attendee__lan__in=lan_payers) & Q(attendee__has_paid=True))
            | Q(ticket__ticket_type__lan__in=lan_payers),
        )
        all_recipients = all_recipients.union(lan_payer_users)

        tickets = fields['tickets']
        ticket_users = User.objects.filter(ticket__ticket_type__in=tickets)
        all_recipients = all_recipients.union(ticket_users)

        teams = fields['teams']
        team_users = User.objects.filter(Q(newteamleader__in=teams) | Q(new_team_members__in=teams))
        all_recipients = all_recipients.union(team_users)

        competitions = fields['competitions']
        competition_users = User.objects.filter(
            Q(newteamleader__participant__competition__in=competitions)
            | Q(new_team_members__participant__competition__in=competitions)
            | Q(participant__competition__in=competitions),
        )
        all_recipients = all_recipients.union(competition_users)

        specific_users = fields['users_parsed']
        all_recipients = all_recipients.union(specific_users)

    all_recipient_count = all_recipients.count()

    # The send button was pressed
    if 'send' in old_form.data:
        message = Mail()
        message.form_id = form_id
        message.subject = subject
        message.content = content
        if everyone:
            # Ignore other recipients if "everyone" is chosen
            message.recipient_everyone = everyone
        else:
            if lan_attendees:
                message.recipient_lan_attendees = lan_attendees
            if lan_payers:
                message.recipient_lan_payers = lan_payers
            if tickets:
                message.recipient_tickets = tickets
            if teams:
                message.recipient_teams = teams
            if competitions:
                message.recipient_competitions = competitions
        message.recipients_total = all_recipient_count
        message.save()

        # Prepare mail
        mail_context = {
            'subject': subject,
            'content': content,
        }
        txt_message = render_to_string('sendmail/email/mail.txt', mail_context, request).strip()
        html_message = render_to_string('sendmail/email/mail.html', mail_context, request).strip()

        # Send all emails using the same connection
        mail_connection = django_mail.get_connection()
        mail_connection.open()

        counter = 0
        for user in all_recipients:
            counter += 1
            if not user.email:
                message.failed_mails += 1
                continue

            email_message = django_mail.EmailMultiAlternatives(
                subject=subject,
                body=txt_message,
                from_email=settings.STUDLAN_FROM_MAIL,
                to=[user.email],
                connection=mail_connection,
            )
            email_message.attach_alternative(html_message, 'text/html')
            try:
                email_message.send()
                message.successful_mails += 1
            except SMTPException:
                message.failed_mails += 1
                continue

            # Save the the message stats regularly so that the sending process can be kept track of
            if counter % 10 == 0:
                message.save()

        mail_connection.close()

        message.done_sending = True
        message.save()

        # Show new form
        messages.success(request, _(u'Successfully attempted to send the message to {user_count} users.').format(user_count=all_recipient_count))
        return SendMessageForm()

    # The preview button was pressed
    else:
        template_context['mail_subject'] = subject
        template_context['mail_content'] = content
        template_context['mail_recipient_count'] = all_recipient_count
        return old_form
