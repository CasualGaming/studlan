# -*- coding: utf-8 -*-

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

import stripe

from apps.lan.models import Ticket, TicketType


def payment(request, ticket_id):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    ticket_type = get_object_or_404(TicketType, pk=ticket_id)

    if request.method == 'POST':
        token = request.POST['stripeToken']

        try:
            # Calls Stripe and raises error if it fails
            stripe.Charge.create(
                # Ticket price is in cents meaning we have to add two zeroes
                amount=ticket_type.price * 100,
                currency='nok',
                card=token,
                description=request.user.email,
            )
            ticket = Ticket()
            ticket.user = request.user
            ticket.ticket_type = ticket_type
            ticket.bought_date = datetime.now()
            ticket.save()

            send_ticket_mail(ticket, request.META['HTTP_HOST'])

            messages.success(request, _(u'Payment complete — confirmation mail sent to ') + request.user.email)
        except stripe.error.CardError, e:
            messages.error(request, e)
            pass

    return HttpResponseRedirect('/')


def send_ticket_mail(ticket, host):
    message = _(u'This is a confirmation on your purchase of a ') + ticket.ticket_type.get_translation().title
    message += _(u' ticket for ') + ticket.ticket_type.lan.title
    message += '\n\n' + _(u'The ticket is linked to ') + ticket.user.get_full_name()
    message += '\n\n' + _(u'More information about the lan can be found at ') + host + '/lan'

    send_mail(_(u'Ticket confirmation'), message, settings.STUDLAN_FROM_MAIL, [ticket.user.email])
