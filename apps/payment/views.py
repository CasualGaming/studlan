# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _

import stripe

from apps.lan.models import Ticket, TicketType


payment_logger = logging.getLogger('payment')


def payment_info_static(request):
    return render(request, 'payment/info.html')


def payment_info(request, ticket_type_id):
    return render(
        request,
        'payment/info.html',
        {
            'ticket_type_id': ticket_type_id,
        })


@login_required()
def payment(request, ticket_type_id):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    ticket_type = get_object_or_404(TicketType, pk=ticket_type_id)

    if request.method == 'POST':
        # Stripe
        error_response = JsonResponse({'error': ''})
    else:
        # User
        error_response = redirect(ticket_type.lan.get_absolute_url())

    if ticket_type.lan.end_date < datetime.now():
        # "The LAN is over" is already visible on the page
        return error_response

    if ticket_type.lan.has_ticket(request.user) or request.user in ticket_type.lan.paid_attendees:
        messages.warning(request, _(u'You already have a ticket for this LAN.'))
        return error_response

    if not ticket_type.is_available():
        messages.warning(request, _(u'This ticket is not yet available.'))
        return error_response

    if ticket_type.is_sold_out():
        messages.warning(request, _(u'All tickets have sold out.'))
        return error_response

    if request.user not in ticket_type.lan.attendees:
        messages.error(request, _(u'You must attend first to buy a ticket for this LAN.'))
        return error_response

    if request.method == 'POST':
        description = u'{lan} {ticket} ticket for {user}'.format(ticket=ticket_type, lan=ticket_type.lan, user=request.user)
        json_data = json.loads(request.body)
        intent = None
        try:
            if 'payment_method_id' in request.body:
                # Create the PaymentIntent
                intent = stripe.PaymentIntent.create(
                    payment_method=str(json_data['payment_method_id']),
                    amount=ticket_type.price * 100,
                    currency='nok',
                    description=description,
                    confirmation_method='manual',
                    confirm=True,
                )
            elif 'payment_intent_id' in request.body:
                intent = stripe.PaymentIntent.confirm(str(json_data['payment_intent_id']))
        except stripe.error.CardError as e:
            messages.error(request, _(e.user_message))
            return JsonResponse({'error': e.user_message})
        return generate_payment_response(request, ticket_type, intent)
    else:
        return render(
            request,
            'payment/checkout.html',
            {
                'ticket_type': ticket_type,
                'lan': ticket_type.lan,
            })


def generate_payment_response(request, ticket_type, intent):
    # Instruct Stripe.js to handle SCA if required
    if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
        return JsonResponse({
            'requires_action': True,
            'payment_intent_client_secret': intent.client_secret,
        })
    elif intent.status == 'succeeded':
        make_ticket(request, ticket_type)
        payment_logger.info('Successful purchase of ticket "%s" "%s" for user "%s".', ticket_type.lan, ticket_type, request.user)
        return JsonResponse({'success': True})
    else:
        payment_logger.info('Failed purchase of ticket "%s" "%s" for user "%s".', ticket_type.lan, ticket_type, request.user, intent.status)
        messages.error(request, _(u'Payment unsuccessful. Please contact support.'))
        return JsonResponse({'error': 'Invalid PaymentIntent status'})


def make_ticket(request, ticket_type):
    # Create ticket
    ticket = Ticket()
    ticket.user = request.user
    ticket.ticket_type = ticket_type
    ticket.bought_date = datetime.now()
    ticket.save()

    # Render templates
    lan = ticket.ticket_type.lan
    lan_link = request.build_absolute_uri(lan.get_absolute_url())
    context = {
        'lan': lan,
        'lan_link': lan_link,
        'ticket': ticket,
    }
    txt_message = render_to_string('payment/email/ticket_receipt.txt', context, request).strip()
    html_message = render_to_string('payment/email/ticket_receipt.html', context, request).strip()

    # Send mail
    from_address = u'"{name}" <{address}>'.format(name=settings.SITE_NAME, address=settings.DEFAULT_FROM_EMAIL)
    to_address = u'"{name}" <{address}>'.format(name=ticket.user.get_full_name(), address=ticket.user.email)
    send_mail(
        from_email=from_address,
        recipient_list=[to_address],
        subject=_(u'Ticket receipt'),
        message=txt_message,
        html_message=html_message,
    )

    messages.success(
        request,
        _(u'Payment complete.'),
    )
