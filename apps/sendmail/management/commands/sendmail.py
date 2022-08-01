# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from smtplib import SMTPException

from django.conf import settings
from django.contrib.sites.models import Site
from django.core import mail as django_mail
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.template.loader import render_to_string

from django_pglocks import advisory_lock

from apps.sendmail.models import Mail, MailRecipient


sendmail_logger = logging.getLogger('sendmail')


class Command(BaseCommand):

    def handle(self, *args, **options):

        sendmail_logger.debug('Checking for pending mail')

        # If using Postgres (as in prod), use a PG advisory lock
        if connection.vendor == 'postgresql':
            with advisory_lock(lock_id='sendmail_send', wait=False) as acquired:
                if not acquired:
                    sendmail_logger.debug('Another instance is already running, exiting')
                    return
                self.send_pending_mails()
        else:
            self.send_pending_mails()


    def send_pending_mails(self):
        # Get pending mails
            pending_mails = Mail.objects.filter(recipients__sent_time=None)
            if len(pending_mails) == 0:
                return

            sendmail_logger.debug('Found pending mails to send')

            # Open shared mail connection
            mail_connection = django_mail.get_connection()
            mail_connection.open()

            # Try to send mails to recipients of all pending mails
            for mail in pending_mails:
                for recipient in MailRecipient.objects.filter(mail=mail, sent_time=None):
                    self.send_recipient_mail(mail, recipient, mail_connection)

            # Close shared mail connection
            mail_connection.close()

    def send_recipient_mail(self, mail, recipient, mail_connection):
        sendmail_logger.info('Sending mail "%s" to user "%s"', mail.uuid, recipient.user.username)

        # Ignore if user doesn't have an email address
        if not recipient.user.email:
            sendmail_logger.warning('Unable to send mail "%s" to user "%s": Missing e-mail address', mail.uuid, recipient.user.username)
            return

        # Render mail
        mail_context = {
            'site_name': settings.SITE_NAME,
            'site_host': Site.objects.get_current().domain,
            'language_code': mail.language,
            'recipient': recipient.user,
            'sender': mail.sender,
            'subject': mail.subject,
            'content': mail.content,
        }
        txt_message = render_to_string('sendmail/email/mail.txt', mail_context).strip()
        html_message = render_to_string('sendmail/email/mail.html', mail_context).strip()

        # Send mail
        from_address = u'"{name}" <{address}>'.format(name=settings.SITE_NAME, address=settings.DEFAULT_FROM_EMAIL)
        to_address = u'"{name}" <{address}>'.format(name=recipient.user.get_full_name(), address=recipient.user.email)
        email_message = django_mail.EmailMultiAlternatives(
            connection=mail_connection,
            from_email=from_address,
            to=[to_address],
            subject=mail.subject,
            body=txt_message,
        )
        email_message.attach_alternative(html_message, 'text/html')
        try:
            email_message.send()
        except SMTPException:
            sendmail_logger.exception('Unable to send mail "%s" to user "%s": An SMTP exception occurred', mail.uuid, recipient.user.username)
            return

        # Mark as sent
        recipient.sent_time = datetime.now()
        recipient.save()
