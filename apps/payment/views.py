# -*- coding: utf-8 -*-

import json
from datetime import datetime

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext as _

from apps.lan.models import Ticket, TicketType


@login_required()
def payment(request, ticket_id):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    ticket_type = get_object_or_404(TicketType, pk=ticket_id)

    if request.method == 'GET':
        return render(
            request,
            'payment/checkout.html',
            {
                'ticket_type': ticket_type,
                'lan': ticket_type.lan,
            })

    if request.method == 'POST':
        json_data = json.loads(request.body)
        intent = None
        try:
            if 'payment_method_id' in request.body:
                # Create the PaymentIntent
                intent = stripe.PaymentIntent.create(
                    payment_method=str(json_data['payment_method_id']),
                    amount=ticket_type.price * 100,
                    currency='nok',
                    confirmation_method='manual',
                    confirm=True,
                )
            elif 'payment_intent_id' in request.body:
                intent = stripe.PaymentIntent.confirm(str(json_data['payment_intent_id']))
        except stripe.error.CardError as e:
            messages.error(request, _(e.user_message))
            return JsonResponse({'error': e.user_message})

        return generate_payment_response(request, ticket_type, intent)

    return HttpResponseRedirect('/')


def generate_payment_response(request, ticket_type, intent):
    if intent.status == 'requires_action' and intent.next_action.type == 'use_stripe_sdk':
        return JsonResponse({
            'requires_action': True,
            'payment_intent_client_secret': intent.client_secret,
        })
    elif intent.status == 'succeeded':

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

        return JsonResponse({'success': True})
    else:
        messages.error(request, _(u'Payment unsuccessful - please contact support'))
        return JsonResponse({'error': 'Invalid PaymentIntent status'})
