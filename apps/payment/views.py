# -*- coding: utf-8 -*-

import json
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_GET, require_POST

import stripe

from apps.lan.models import Ticket, TicketType
from apps.payment.models import LANTicketPurchaseLock


def payment_info_static(request):
    return render(request, 'payment/info.html')


def payment_info(request, ticket_type_id):
    return render(
        request,
        'payment/info.html',
        {
            'ticket_type_id': ticket_type_id,
        })


@require_GET
@login_required
def payment(request, ticket_type_id):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    ticket_type = get_object_or_404(TicketType, pk=ticket_type_id)

    if not check_payment_allowed(request, ticket_type):
        return redirect('lan_details', lan_id=ticket_type.lan_id)

    return render(
        request,
        'payment/checkout.html',
        {
            'ticket_type': ticket_type,
            'lan': ticket_type.lan,
        })


@require_POST
@login_required
def make_payment(request, ticket_type_id):
    ticket_type = get_object_or_404(TicketType, pk=ticket_type_id)

    if not check_payment_allowed(request, ticket_type):
        return JsonResponse({'error': ''})

    # Lock wrt. LAN
    LANTicketPurchaseLock.objects.get_or_create(lan=ticket_type.lan)
    lock = LANTicketPurchaseLock.objects.select_for_update().filter(lan=ticket_type.lan)
    with transaction.atomic():
        lock[0].evaluate()
        return make_payment_unsafe(request, ticket_type)


def make_payment_unsafe(request, ticket_type):
    """Not thread-safe."""

    description = u'{lan} {ticket} ticket for {user}'.format(ticket=ticket_type, lan=ticket_type.lan, user=request.user)
    intent = None

    # Check again in case anything changed while waiting
    if not check_payment_allowed(request, ticket_type):
        return JsonResponse({'error': ''})

    try:
        json_data = json.loads(request.body)
    except ValueError:
        return JsonResponse({'error': ''})

    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    # When the client has filled in card details and presses the pay button
    if 'payment_method_id' in request.body:
        try:
            # Create the PaymentIntent
            intent = stripe.PaymentIntent.create(
                payment_method=str(json_data['payment_method_id']),
                amount=ticket_type.price * 100,
                currency='nok',
                description=description,
                confirmation_method='manual',
                confirm=True,
            )
            # Instruct Stripe.js to handle SCA if required
            if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
                return JsonResponse({
                    'requires_action': True,
                    'payment_intent_client_secret': intent.client_secret,
                })
        except stripe.error.StripeError as e:
            messages.error(request, _(u'Payment failed: ') + e.user_message)
            return JsonResponse({'error': e.user_message})

    # When the payment intent is ready to be confirmed after SCA succeeds
    if 'payment_intent_id' in request.body:
        try:
            intent = stripe.PaymentIntent.confirm(str(json_data['payment_intent_id']))
        except stripe.error.StripeError as e:
            messages.error(request, _(u'Payment failed: ') + e.user_message)
            return JsonResponse({'error': e.user_message})

    if intent and intent.status == 'succeeded':
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

        messages.success(
            request,
            _(u'Payment complete.'),
        )

        return JsonResponse({'success': True})

    else:
        messages.error(request, _(u'Payment unsuccessful.'))
        return JsonResponse({'error': 'Invalid payment intent status'})


def check_payment_allowed(request, ticket_type):
    if ticket_type.lan.end_date < datetime.now():
        # "The LAN is over" is already visible on the page
        return False

    if ticket_type.lan.has_ticket(request.user) or request.user in ticket_type.lan.paid_attendees:
        messages.info(request, _(u'You already have a ticket for this LAN.'))
        return False

    if not ticket_type.is_available():
        messages.info(request, _(u'This ticket is not yet available.'))
        return False

    if ticket_type.is_sold_out():
        messages.info(request, _(u'All tickets have sold out.'))
        return False

    if request.user not in ticket_type.lan.attendees:
        messages.info(request, _(u'You must attend first to buy a ticket for this LAN.'))
        return False

    return True
