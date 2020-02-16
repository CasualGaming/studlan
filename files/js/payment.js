var stripe = Stripe(stripe_public_key);

var elements = stripe.elements();
var cardElement = elements.create(
    'card',
    {
        hidePostalCode: true
    });
cardElement.mount('#card-element');

var cardForm = document.getElementById('card-form');
var cardholderName = document.getElementById('cardholder-name');
var cardButton = document.getElementById('card-button');
var testSubmit = document.getElementById('test-submit');

cardForm.addEventListener('submit', function(ev) {
  // Prevent real submit
  ev.preventDefault();

  if (!cardholderName.value) {
    // Use extra submit button to force native form validation
    // Since the field is empty, it won't submit
    testSubmit.click();
    return;
  }

  // Ignore any type of submit if the button is disabled
  if (cardButton.disabled) {
    return;
  }

  cardButton.disabled = true;
  stripe.createPaymentMethod('card', cardElement, {
    billing_details: {name: cardholderName.value}
  }).then(function(result) {
    if (result.error) {
      console.error(result.error);
      // Allow user to submit again
      cardButton.disabled = false;
    } else {
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