"""Price lookup. Used by the checkout page and by the nightly invoice job."""
import json
from pathlib import Path

RATES = json.loads((Path(__file__).parent / "rates.json").read_text())


def price(plan, currency):
    """Price of a plan in `currency`, in the units the payment processor wants."""
    base = RATES["plans"][plan]                 # always in USD cents
    rate = RATES["fx"][currency]                # target currency per USD
    return round(base * rate)
