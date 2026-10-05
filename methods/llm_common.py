"""Shared prompt and run loop for the LLM methods (2 and 3)."""
import csv
import json
import re
import time
from decimal import Decimal, InvalidOperation

from methods.method1_rules import PDF_DIR, ROOT, pdf_text
from schema import AMOUNT_FIELDS, FIELDS, write_csv

USAGE_FIELDS = ["invoice_id", "model", "input_tokens", "output_tokens", "seconds", "cost_usd", "error"]

PROMPT = """Extract the following fields from the invoice text below and return them as a single JSON object. Output JSON only: no explanation, no markdown.

Fields:
- invoice_id: the invoice (or credit note) number.
- vendor: name of the company issuing the invoice.
- vendor_country: the vendor's country as an ISO 3166-1 alpha-2 code (e.g. "DE").
- recipient: name of the company the invoice is billed to.
- recipient_country: the recipient's country as an ISO 3166-1 alpha-2 code.
- date: invoice date, ISO format YYYY-MM-DD.
- due_date: due date, ISO format YYYY-MM-DD.
- currency: ISO 4217 code (e.g. "EUR").
- subtotal: the subtotal printed on the invoice, net of VAT. If the printed subtotal includes VAT, subtract the VAT amount from it.
- vat_rate: the VAT rate as a fraction (20% is 0.20). If the rate is not stated but a VAT amount is printed, derive it from VAT amount / subtotal. Use null if the invoice does not let you determine it or if more than one rate applies. Use 0.00 under reverse charge.
- vat_amount: the VAT amount printed on the invoice; if several VAT amounts are printed, their sum. If prices include VAT and no VAT amount is printed, the VAT contained in the line items at the stated rate. Use null if it cannot be determined. Use 0.00 under reverse charge.
- discount_amount: the discount deducted on the invoice, as a positive number. Use 0.00 if no discount is deducted.
- total: the total printed on the invoice.
- is_credit_note: true if the document is a credit note, otherwise false.
- arithmetic_flag: true only if the printed figures do not add up, i.e. the line items do not sum to the printed subtotal, or subtotal plus VAT minus discount does not equal the printed total. Otherwise false.

Amounts are the values printed on the invoice, even if they look wrong: copy them, do not correct them. Keep the printed sign. Write amounts as plain JSON numbers with a dot as decimal separator and two decimals, without thousands separators or currency symbols. Use null for any field that cannot be determined.

Invoice text:
"""


def parse_row(reply):
    """LLM reply -> schema row. Values the schema cannot hold are blanked, not repaired."""
    data = json.loads(re.search(r"\{.*\}", reply, re.S).group())
    row = {f: data.get(f) for f in FIELDS}
    for f in AMOUNT_FIELDS + ["vat_rate"]:
        try:
            row[f] = None if row[f] is None else Decimal(str(row[f]))
        except InvalidOperation:
            row[f] = None
    return row


def _read(path):
    if not path.exists():
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {r["invoice_id"]: r for r in csv.DictReader(f)}


def run(method, call, prompt=PROMPT, parse=parse_row):
    """Run `call` over all invoices, resuming from earlier runs.

    call(prompt) -> (reply_text, usage_dict with any of model/input_tokens/output_tokens/cost_usd)
    Invoices with a usage row and no error are skipped; failed ones are retried.
    """
    out_csv = ROOT / "outputs" / f"{method}.csv"
    usage_csv = ROOT / "results" / f"{method.split('_')[0]}_usage.csv"
    rows, usage = _read(out_csv), _read(usage_csv)
    for pdf in sorted(PDF_DIR.glob("*.pdf")):
        inv = pdf.stem
        if inv in usage and not usage[inv]["error"]:
            continue
        row, u, start = {}, {}, time.time()
        try:
            reply, u = call(prompt + pdf_text(pdf))
            row = parse(reply)
        except Exception as e:  # one bad call must not stop the run: empty row, error logged
            u["error"] = f"{type(e).__name__}: {e}"[:300].replace("\n", " ")
        row["invoice_id"] = inv  # keyed by file name so a misread number cannot drop the row
        rows[inv] = row
        usage[inv] = {"invoice_id": inv, "seconds": f"{time.time() - start:.1f}", **u}
        print(inv, usage[inv].get("model", ""), usage[inv].get("error", "ok"), flush=True)

        write_csv(out_csv, [rows[k] for k in sorted(rows)])
        usage_csv.parent.mkdir(exist_ok=True)
        with open(usage_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, USAGE_FIELDS, restval="")
            w.writeheader()
            w.writerows(usage[k] for k in sorted(usage))
    failed = sum(bool(u.get("error")) for u in usage.values())
    print(f"{len(usage) - failed}/{len(usage)} invoices ok, {failed} failed -> {out_csv}")
