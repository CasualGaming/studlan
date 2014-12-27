import stripe

from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

def payment(request):
    stripe.api_key = settings.STRIPE_PRIVATE_KEY

    if request.method == "POST":
        token = request.POST['stripeToken']

        try:
            charge = stripe.Charge.create(
                amount=5000,
                currency="nok",
                card=token,
                description="payinguser@example.com"
            )
            #TODO create payment object
            messages.success(request, "Payment complete")
        except stripe.CardError, e:
            messages.error(request, e)
            pass

    return redirect('/')
        
    


