"""Nightly invoice job. Writes the amount the card is actually charged."""
from prices import price


def charge_amount(plan, currency):
    """What we hand to the payment processor."""
    return price(plan, currency)
