"""Method 1: pdfplumber text + regex/rules, no LLM.

Run from the repo root: py -m methods.method1_rules
"""
import re
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import pdfplumber

from schema import write_csv

ROOT = Path(__file__).resolve().parent.parent
CENT = Decimal("0.01")

# 1.234,56 (german) / 1'234.56 (swiss) / 1,234.56 (english) / 1234.56
NUM = r"(?<![\d.,'’])(?:\d{1,3}(?:[.,'’]\d{3})+|\d+)[.,]\d{2}(?!\d)"
# sign may sit before the currency ("-EUR 645.94") or before the digits ("EUR -645.94")
MONEY = rf"-?(?:(?:EUR|USD|GBP|CHF)\s*)?-?{NUM}"

COUNTRIES = {
    "austria": "AT", "belgium": "BE", "czech republic": "CZ", "denmark": "DK",
    "estonia": "EE", "finland": "FI", "france": "FR", "germany": "DE",
    "ireland": "IE", "italy": "IT", "latvia": "LV", "lithuania": "LT",
    "luxembourg": "LU", "netherlands": "NL", "norway": "NO", "poland": "PL",
    "portugal": "PT", "spain": "ES", "sweden": "SE", "switzerland": "CH",
    "united kingdom": "GB",
}
DATE_FORMATS = ["%d %B %Y", "%d %b %Y", "%B %d, %Y", "%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d"]


def to_dec(s):
    # ponytail: MONEY only matches amounts with exactly two decimals, so the
    # separators carry no information: digits / 100. Needs real separator
    # logic if invoices ever print whole or 3-decimal amounts.
    value = Decimal(re.sub(r"\D", "", s)) / 100
    return -value if "-" in s else value


def amounts(s):
    return [to_dec(m) for m in re.findall(MONEY, s)]


def to_date(s):
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    return None


def extract(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    flat = " ".join(lines)
    row = {}

    # --- header: "<vendor> Invoice No: <id>", "... Date: <d>", "... Due: <d>", then vendor country
    if m := re.search(r"^(.+?)\s+(?:Invoice|Credit Note) No:\s*(\S+)", text, re.M):
        row["vendor"], row["invoice_id"] = m.group(1), m.group(2)
    if m := re.search(r"\bDate:\s*(.+)$", text, re.M):
        row["date"] = to_date(m.group(1))
    if m := re.search(r"\bDue:\s*(.+)$", text, re.M):
        row["due_date"] = to_date(m.group(1))
    due = next((i for i, l in enumerate(lines) if re.search(r"\bDue:", l)), None)
    if due is not None:
        row["vendor_country"] = next(
            (COUNTRIES[l.lower()] for l in lines[due + 1:due + 3] if l.lower() in COUNTRIES), None)

    # --- recipient block: "Bill to:" / name / street / "<postcode> <city>, <country>"
    if "Bill to:" in lines:
        block = lines[lines.index("Bill to:") + 1:][:4]
        row["recipient"] = block[0] if block else None
        row["recipient_country"] = next(
            (COUNTRIES[l.rsplit(",", 1)[-1].strip().lower()] for l in block[1:]
             if l.rsplit(",", 1)[-1].strip().lower() in COUNTRIES), None)

    if m := re.search(r"\b(EUR|USD|GBP|CHF)\b", flat):
        row["currency"] = m.group(1)
    row["is_credit_note"] = bool(re.search(r"credit note", flat, re.I))

    # --- line items: table rows "<desc> <qty> <unit> <amount>", or paragraph
    # sentences "... = <amount>" / "... we invoice <amount>" (these can wrap, so use flat text)
    table_row = rf"^.+\s\d+\s+{MONEY}\s+({MONEY})$"
    items = [to_dec(a) for a in re.findall(table_row, text, re.M)]
    items += [to_dec(a) for a in re.findall(rf"(?:=|we invoice)\s*({MONEY})", flat)]
    line_sum = sum(items) if items else None

    # --- summary lines, classified by keyword; the amount is the last one on the line
    subtotal = total = vat = None
    discount = Decimal(0)
    rates = set()
    for l in lines:
        if re.match(table_row, l) or "we invoice" in l or "×" in l or l.startswith(("Payment terms", "Bank")):
            continue
        low, amts = l.lower(), amounts(l)
        if re.match(r"(the )?subtotal\b", low):
            subtotal = amts[-1] if amts else subtotal
        elif re.search(r"discount|rebate|adjustment", low):
            if amts:
                discount += abs(amts[-1])  # printed as "-X" or "(X)"; stored positive
        elif re.search(r"\bvat\b", low):
            if m := re.search(r"(\d+(?:[.,]\d+)?)\s*%", l):
                rates.add(Decimal(m.group(1).replace(",", ".")) / 100)
            if amts:
                vat = (vat or 0) + amts[-1]
        elif re.search(r"\btotal\b", low) and amts:
            total = amts[-1]

    rate = rates.pop() if len(rates) == 1 else None  # several rates = mixed VAT, no single rate
    vat_included = bool(re.search(r"incl(?:\.|uding|udes?)\s.{0,10}VAT", flat, re.I))
    printed_subtotal = subtotal

    if "reverse charge" in flat.lower():
        rate, vat = Decimal(0), Decimal(0)
    elif vat_included:
        # Printed subtotal is gross. VAT is the VAT contained in the line items
        # (fall back to the printed gross subtotal); net subtotal = gross - VAT.
        gross = line_sum if line_sum is not None else subtotal
        if rate is not None and gross is not None:
            vat = (gross * rate / (1 + rate)).quantize(CENT, ROUND_HALF_UP)
            if subtotal is not None:
                subtotal -= vat
    elif rate is None and not rates and vat is not None and subtotal:
        rate = (vat / subtotal).quantize(CENT, ROUND_HALF_UP)  # rate not printed: derive it

    # --- arithmetic: line items must sum to the printed subtotal, and
    # subtotal (+ VAT unless already included) - discount must equal the total
    flag = False
    if printed_subtotal is not None:
        if line_sum is not None and abs(line_sum - printed_subtotal) > CENT:
            flag = True
        if total is not None:
            expected = printed_subtotal + (0 if vat_included else vat or 0) - discount
            flag = flag or abs(expected - total) > CENT

    row.update(subtotal=subtotal, vat_rate=rate, vat_amount=vat, discount_amount=discount,
               total=total, arithmetic_flag=flag)
    return row


def main():
    assert to_dec("1.234,56") == to_dec("1'234.56") == to_dec("1,234.56") == Decimal("1234.56")
    assert amounts("Discount (5%): -EUR 645.94") == [Decimal("-645.94")]
    assert amounts("ref. FA-2021-895 (-2.5%): -2.082,54 EUR") == [Decimal("-2082.54")]

    rows = []
    for pdf in sorted((ROOT / "data" / "pdf").glob("*.pdf")):
        with pdfplumber.open(pdf) as doc:
            text = "\n".join(page.extract_text() or "" for page in doc.pages)
        row = extract(text)
        row.setdefault("invoice_id", pdf.stem)
        rows.append(row)
    out = ROOT / "outputs" / "method1_rules.csv"
    write_csv(out, rows)
    print(f"wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
