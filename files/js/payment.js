var stripe = Stripe(stripe_public_key);

var elements = stripe.elements();
var cardElement = elements.create(
    'card',
    {
        hidePostalCode: true
    });
cardElement.mount('#card-element');

var cardholderName = document.getElementById('cardholder-name');
var cardButton = document.getElementById('card-button');

cardButton.addEventListener('click', function(ev) {
  stripe.createPaymentMethod('card', cardElement, {
    billing_details: {name: cardholderName.value}
  }).then(function(result) {
    if (result.error) {
    } else {
      cardButton.disabled = true;
      fetch(payment_url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf_token},
        body: JSON.stringify({payment_method_id: result.paymentMethod.id})})
          .then(function(result) {
        // Handle server response (see Step 3)
        result.json().then(function(json) {
          handleServerResponse(json);
        })
      });
    }
  });
});

function handleServerResponse(response) {
  if (response.error) {
    setTimeout(function () {
                window.location.href = lan_url;
          }, 100);
  } else if (response.requires_action) {
    stripe.handleCardAction(
      response.payment_intent_client_secret
    ).then(function(result) {
      if (result.error) {
          setTimeout(function () {
                window.location.href = lan_url;
          }, 100);
      } else {
        fetch(payment_url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf_token},
          body: JSON.stringify({ payment_intent_id: result.paymentIntent.id })
        }).then(function(confirmResult) {
          return confirmResult.json();
        }).then(handleServerResponse);
      }
    });
  } else {
      setTimeout(function () {
           window.location.href = lan_url;
      }, 100);
  }
}