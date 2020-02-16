# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

#import mailer

from apps.misc.forms import InlineSpanErrorList
from apps.userprofile.models import User

from .forms import SendMessageForm
from .models import Mail


@login_required
@permission_required('sendmail.send_mail')
def sendmail_send(request):
    context = {}

    if request.method == 'POST':
        form = SendMessageForm(request.POST, error_class=InlineSpanErrorList)
        if form.is_valid():
            fields = form.cleaned_data
            subject = fields['subject']
            content = fields['content']
            everyone = fields['everyone']
            yourself = fields['yourself']
            lan_attendees = fields['lan_attendees']
            lan_attendee_users = User.objects.filter(attendee__lan__in=lan_attendees)
            lan_payers = fields['lan_payers']
            lan_payer_users = User.objects.filter(
                (Q(attendee__lan__in=lan_payers) & Q(attendee__has_paid=True))
                | Q(ticket__ticket_type__lan__in=lan_payers),
            )
            tickets = fields['tickets']
            ticket_users = User.objects.filter(ticket__ticket_type__in=tickets)
            teams = fields['teams']
            team_users = User.objects.filter(Q(newteamleader__in=teams) | Q(new_team_members__in=teams))
            competitions = fields['competitions']
            competition_users = User.objects.filter(
                Q(newteamleader__participant__competition__in=competitions)
                | Q(new_team_members__participant__competition__in=competitions)
                | Q(participant__competition__in=competitions),
            )
            specific_users = fields['users_parsed']

            # Aggregate users
            if everyone:
                all_recipients = User.objects.all()
            else:
                # competition_users breaks on "|" but not "union" for some reason
                all_recipients = lan_attendee_users | lan_payer_users | ticket_users | team_users | specific_users.union(competition_users)
                if yourself:
                    all_recipients = all_recipients | User.objects.filter(id=request.user.id)
            all_recipient_count = all_recipients.count()

            if 'send' in form.data:
                mail = Mail()
                mail.subject = subject
                mail.content = content
                if everyone:
                    # Ignore other recipients if "everyone" is chosen
                    mail.recipient_everyone = everyone
                else:
                    if lan_attendees:
                        mail.recipient_lan_attendees = lan_attendees
                    if lan_payers:
                        mail.recipient_lan_payers = lan_payers
                    if tickets:
                        mail.recipient_tickets = tickets
                    if teams:
                        mail.recipient_teams = teams
                    if competitions:
                        mail.recipient_competitions = competitions
                mail.save()

                # Prepare mail
                context = {
                    'subject': subject,
                    'content': content,
                }
                txt_message = render_to_string('sendmail/email/mail.txt', context, request).strip()
                html_message = render_to_string('sendmail/email/mail.html', context, request).strip()

                # Send to all users
                successful_recipient_count = 0
                for user in all_recipients:
                    if not user.email:
                        continue
                    successful_recipient_count += 1
                    # TODO use django-mailer
                    send_mail(
                        subject=subject,
                        from_email=settings.STUDLAN_FROM_MAIL,
                        recipient_list=[user.email],
                        message=txt_message,
                        html_message=html_message,
                    )

                # Show new form
                form = SendMessageForm()
                messages.success(request, _(u'Successfully sent the message to {success} of {all} users.').format(success=successful_recipient_count, all=all_recipient_count))
            elif 'preview' in form.data:
                context['mail_subject'] = subject
                context['mail_content'] = content
                context['mail_recipient_count'] = all_recipient_count

    else:
        form = SendMessageForm()

    context['form'] = form
    return render(request, 'sendmail/send.html', context)
