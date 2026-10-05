"""Method 4 reconciliation check. No API calls."""
from decimal import Decimal

from methods.method4_hybrid import reconcile_rate

# INV-2026-0038 as output by the first method 4 run (commit 05ff2bb): the invoice
# prints no VAT rate, and the 5% of its early payment discount came back as the rate.
VAT_AMOUNT = Decimal("63676.30")
NET_SUBTOTAL = Decimal("318381.50")


def test_wrong_transcribed_rate_is_overridden():
    rate, override = reconcile_rate(Decimal("0.05"), VAT_AMOUNT, NET_SUBTOTAL)
    assert rate == Decimal("0.20")
    assert override == "0.05 -> 0.20"


def test_agreeing_rate_is_kept():
    assert reconcile_rate(Decimal("0.20"), VAT_AMOUNT, NET_SUBTOTAL) == (Decimal("0.20"), None)


def test_nothing_to_reconcile_without_rate_or_amounts():
    assert reconcile_rate(None, VAT_AMOUNT, NET_SUBTOTAL) == (None, None)
    assert reconcile_rate(Decimal("0.20"), None, NET_SUBTOTAL) == (Decimal("0.20"), None)
