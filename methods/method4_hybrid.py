"""Method 4: hybrid. The LLM only transcribes; Python does all arithmetic and judgement.

Run from the repo root: py -m methods.method4_hybrid
"""
import json
import os
import re
import time
from decimal import ROUND_HALF_UP, Decimal

from dotenv import load_dotenv
from google import genai
from google.genai import errors

from methods.llm_common import run
from methods.method1_rules import CENT, COUNTRIES, ROOT, to_date

MODEL = "gemini-3.1-flash-lite-preview"  # one model only: retry on 503/429, never switch
BACKOFF = [15, 30, 60, 120, 240]

PROMPT = """Transcribe the invoice text below into a single JSON object. Output JSON only: no explanation, no markdown.

You are a transcriber. Copy what is printed. Never calculate, correct, convert or fill in a missing value. If something is not printed, use null (or an empty list). Copy every amount exactly as printed, as a string, including its sign and its thousands and decimal separators (for example "1.234,56" or "-3'107.01").

Fields:
- invoice_id: the invoice or credit note number.
- vendor: name of the company issuing the invoice.
- vendor_country: the vendor's country as printed.
- recipient: name of the company the invoice is billed to.
- recipient_country: the recipient's country as printed.
- date: the invoice date as printed.
- due_date: the due date as printed.
- currency: the currency code as printed.
- line_items: a list with one object per invoiced item: {"description", "quantity", "unit_price", "amount"}. Use null for a part that is not printed.
- subtotal: the printed subtotal amount.
- subtotal_includes_vat: true if the invoice states that the subtotal or the prices include VAT, otherwise false.
- vat_rates: a list of every VAT percentage printed anywhere on the invoice, as printed (for example ["20%"]). Empty list if no VAT percentage is printed.
- vat_amounts: a list of every printed VAT amount. Empty list if no VAT amount is printed.
- reverse_charge_wording: the printed sentence saying that reverse charge applies, or null.
- discount_amount: the printed amount of a discount, rebate or similar deduction, or null.
- discount_wording: the printed wording of that deduction, or null.
- total: the printed total amount.
- credit_note_wording: the printed wording identifying the document as a credit note, or null.

Invoice text:
"""


load_dotenv(ROOT / ".env", encoding="utf-8-sig")  # utf-8-sig: the file may start with a BOM
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def parse_amount(s):
    """Printed amount -> Decimal. The decimal separator is the last . or ,
    followed by exactly two digits; everything else (' . , space) groups thousands."""
    if s is None or not re.search(r"\d", str(s)):
        return None
    s = str(s)
    body = re.sub(r"[^\d.,]", "", s).rstrip(".,")  # drops currency, spaces, ', sign, sentence full stop
    m = re.fullmatch(r"(.*)[.,](\d{2})", body)
    whole, cents = (m.group(1), m.group(2)) if m else (body, "00")
    value = Decimal(re.sub(r"\D", "", whole) or "0") + Decimal(cents) / 100
    return -value if "-" in s else value


def country(s):
    s = (s or "").strip()
    return COUNTRIES.get(s.lower()) or (s.upper() if len(s) == 2 else None)


def build_row(reply):
    t = json.loads(re.search(r"\{.*\}", reply, re.S).group())  # the transcription

    item_amounts = [parse_amount(i.get("amount")) for i in t.get("line_items") or []]
    line_sum = sum(item_amounts) if item_amounts and None not in item_amounts else None
    printed_subtotal = parse_amount(t.get("subtotal"))
    total = parse_amount(t.get("total"))
    discount = abs(parse_amount(t.get("discount_amount")) or Decimal(0))
    vat_amounts = [a for a in map(parse_amount, t.get("vat_amounts") or []) if a is not None]
    vat = sum(vat_amounts) if vat_amounts else None
    rates = {Decimal(m.group(1).replace(",", ".")) / 100
             for r in t.get("vat_rates") or [] if (m := re.search(r"(\d+(?:[.,]\d+)?)", str(r)))}
    rate = rates.pop() if len(rates) == 1 else None  # several rates = mixed VAT, no single rate
    included = bool(t.get("subtotal_includes_vat"))
    subtotal = printed_subtotal

    if t.get("reverse_charge_wording"):
        rate, vat = Decimal(0), Decimal(0)
    elif included:
        # Line items and printed subtotal are gross. VAT is the VAT contained in the
        # line items; net subtotal = printed gross subtotal - VAT (as method 1 does).
        gross = line_sum if line_sum is not None else printed_subtotal
        if rate is not None and gross is not None:
            vat = (gross * rate / (1 + rate)).quantize(CENT, ROUND_HALF_UP)
            if subtotal is not None:
                subtotal -= vat
    elif rate is None and not rates and vat is not None and subtotal:
        rate = (vat / subtotal).quantize(CENT, ROUND_HALF_UP)  # rate not printed: derive it

    flag = False
    if printed_subtotal is not None:
        if line_sum is not None and abs(line_sum - printed_subtotal) > CENT:
            flag = True
        if total is not None:
            expected = printed_subtotal + (0 if included else vat or 0) - discount
            flag = flag or abs(expected - total) > CENT

    return {
        "vendor": t.get("vendor"), "vendor_country": country(t.get("vendor_country")),
        "recipient": t.get("recipient"), "recipient_country": country(t.get("recipient_country")),
        "date": to_date(str(t.get("date") or "")), "due_date": to_date(str(t.get("due_date") or "")),
        "currency": t.get("currency"), "subtotal": subtotal, "vat_rate": rate, "vat_amount": vat,
        "discount_amount": discount, "total": total,
        "is_credit_note": bool(t.get("credit_note_wording")), "arithmetic_flag": flag,
    }


def call(prompt):
    for wait in BACKOFF + [None]:
        try:
            resp = client.models.generate_content(model=MODEL, contents=prompt)
        except errors.APIError as e:
            if e.code in (429, 503) and wait:
                time.sleep(wait)
                continue
            raise
        finally:
            time.sleep(5)  # free-tier rate limit
        um = resp.usage_metadata
        return resp.text, {
            "model": MODEL,
            "input_tokens": um.prompt_token_count,
            "output_tokens": (um.candidates_token_count or 0) + (um.thoughts_token_count or 0),
        }


if __name__ == "__main__":
    assert parse_amount("1.234,56") == parse_amount("1'234.56 EUR") == parse_amount("EUR 1,234.56.") == Decimal("1234.56")
    assert parse_amount("-EUR 645.94") == Decimal("-645.94") and parse_amount("1.234") == Decimal("1234")
    assert parse_amount("EUR -66,351.10") == Decimal("-66351.10") and parse_amount(None) is None
    run("method4_hybrid", call, PROMPT, build_row)
