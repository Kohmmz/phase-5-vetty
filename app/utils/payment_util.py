import stripe
import os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def process_payment(payment_data):
    """
    Process payment using Stripe.
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(payment_data["amount"] * 100),  # Convert to cents
            currency="usd",
            payment_method_types=["card"],
        )
        return "Completed"
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return "Failed"