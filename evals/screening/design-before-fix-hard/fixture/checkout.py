"""What the customer sees on the checkout page."""
from prices import price

SYMBOL = {"USD": "$", "JPY": "¥"}


def line(plan, currency):
    amount = price(plan, currency)
    if currency == "JPY":
        return f"{SYMBOL[currency]}{amount:,}"        # yen is never written with decimals
    return f"{SYMBOL[currency]}{amount / 100:,.2f}"
