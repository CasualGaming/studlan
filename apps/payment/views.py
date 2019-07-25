# -*- coding: utf-8 -*-

from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
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
        except stripe.error.CardError, e:
            messages.error(request, e)
        else:
            ticket = Ticket()
            ticket.user = request.user
            ticket.ticket_type = ticket_type
            ticket.bought_date = datetime.now()
            ticket.save()

            lan = ticket.ticket_type.lan
            lan_link = request.build_absolute_uri(reverse('lan_details', kwargs={'lan_id': lan.id}))
            context = {
                'ticket': ticket,
                'lan': lan,
                'lan_link': lan_link,
            }
            txt_message = render_to_string('payment/email/ticket_receipt.txt', context, request).strip()
            html_message = render_to_string('payment/email/ticket_receipt.html', context, request).strip()
            send_mail(
                subject=_(u'Ticket confirmation'),
                from_email=settings.STUDLAN_FROM_MAIL,
                recipient_list=[ticket.user.email],
                message=txt_message,
                html_message=html_message,
            )

            messages.success(request, _(u'Payment complete — Confirmation mail sent to ') + request.user.email)

    return HttpResponseRedirect('/')
