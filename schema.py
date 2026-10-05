"""Shared output schema for all extraction methods: one CSV row per invoice."""
import csv
from decimal import Decimal
from pathlib import Path

FIELDS = [
    "invoice_id", "vendor", "vendor_country", "recipient", "recipient_country",
    "date", "due_date", "currency", "subtotal", "vat_rate", "vat_amount",
    "discount_amount", "total", "is_credit_note", "arithmetic_flag",
]
AMOUNT_FIELDS = ["subtotal", "vat_amount", "discount_amount", "total"]
BOOL_FIELDS = ["is_credit_note", "arithmetic_flag"]


def _fmt(field, value):
    if value is None or value == "":
        return ""
    if field in AMOUNT_FIELDS or field == "vat_rate":
        return f"{Decimal(str(value)):.2f}"
    if field in BOOL_FIELDS:
        return str(value).strip().lower() if isinstance(value, str) else str(bool(value)).lower()
    return str(value)  # dates: pass date objects or ISO strings


def write_csv(path, rows):
    """rows: dicts keyed by FIELDS; missing/None values are written empty."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(FIELDS)
        for row in rows:
            w.writerow([_fmt(k, row.get(k)) for k in FIELDS])
