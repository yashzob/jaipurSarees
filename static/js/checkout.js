document.addEventListener('DOMContentLoaded', function() {
    // Get payment method elements
    const stripeRadio = document.getElementById('stripe');
    const codRadio = document.getElementById('cod');
    const stripePaymentSection = document.getElementById('stripe-payment');
    const codPaymentSection = document.getElementById('cod-payment');
    const form = document.getElementById('form');
    // Handle payment method selection
    function handlePaymentMethodChange() {
        if (stripeRadio.checked) {
            stripePaymentSection.style.display = 'block';
            codPaymentSection.style.display = 'none';
        } else {
            stripePaymentSection.style.display = 'none';
            codPaymentSection.style.display = 'block';
        }
    }

    // Initialize payment method display
    handlePaymentMethodChange();

    // Listen for payment method changes
    stripeRadio.addEventListener('change', handlePaymentMethodChange);
    codRadio.addEventListener('change', handlePaymentMethodChange);

    // Handle COD order completion
    const codButton = document.getElementById('complete-order-cod');
    
    if (codButton) {
        codButton.addEventListener('click', function() {
            // Get the form element
            console.log("injas")
            const form = document.getElementById('form');
            
            // Validate required fields
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                alert('Please fill in all required fields');
                return;
            }

            // Create form data and append payment method
            const formData = new FormData(form);
            formData.append('payment_method', 'cod');
            
            // Show loading state
            codButton.disabled = true;
            codButton.textContent = 'Processing...';
            
            // Get CSRF token - try multiple ways to be robust
            function getCSRFToken() {
                const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
                if (csrfInput) return csrfInput.value;
                
                const csrfCookie = document.cookie.match(/csrftoken=([^;]+)/);
                if (csrfCookie) return csrfCookie[1];
                
                console.error('Could not find CSRF token');
                return null;
            }

            const csrfToken = getCSRFToken();
            if (!csrfToken) {
                alert('Security error: Please refresh the page and try again');
                return;
            }

            // Submit the form data
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                } else {
                    return response.json().then(data => {
                        if (data.success) {
                            window.location.href = data.redirect_url;
                        } else {
                            alert('Error completing order: ' + data.error);
                        }
                    });
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while processing your order');
            })
            .finally(() => {
                codButton.disabled = false;
                codButton.textContent = 'Place Order (COD)';
            });
        });
    }

    // Initialize Stripe elements if Stripe is being used
    if (typeof Stripe !== 'undefined') {
        const stripe = Stripe('YOUR_STRIPE_PUBLIC_KEY');
        const elements = stripe.elements();
        const cardElement = elements.create('card');
        cardElement.mount('#card-element');

        // Handle Stripe form submission
        form.addEventListener('submit', function(e) {
            if (!stripeRadio.checked) return;
            
            e.preventDefault();
            
            stripe.createPaymentMethod({
                type: 'card',
                card: cardElement,
                billing_details: {
                    name: form.querySelector('[name="name"]').value,
                    email: form.querySelector('[name="email"]').value
                }
            }).then(function(result) {
                if (result.error) {
                    document.getElementById('card-errors').textContent = result.error.message;
                } else {
                    // Add payment method ID to form and submit
                    const paymentMethodInput = document.createElement('input');
                    paymentMethodInput.setAttribute('type', 'hidden');
                    paymentMethodInput.setAttribute('name', 'stripe_payment_method');
                    paymentMethodInput.setAttribute('value', result.paymentMethod.id);
                    form.appendChild(paymentMethodInput);
                    
                    form.submit();
                }
            });
        });
    }
});
