"""Compare a method CSV with the ground truth, field by field.

Usage: py evaluate.py outputs/method1_rules.csv
Writes results/<method>_eval.md and results/<method>_errors.csv,
where <method> is the CSV name up to the first underscore.
"""
import csv
import json
import sys
import unicodedata
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

from schema import AMOUNT_FIELDS, BOOL_FIELDS, FIELDS

ROOT = Path(__file__).resolve().parent
COMPARED = [f for f in FIELDS if f != "invoice_id"]  # invoice_id is the join key
VARIANT_KEYS = ["vat_variant", "discount_variant", "number_format", "layout", "consistency", "edge_case"]


def expected_row(gt):
    """Ground-truth JSON -> the shared schema (as strings, empty for null)."""
    row = {f: gt.get(f) for f in FIELDS}
    row["subtotal"] = gt["rendered_subtotal"]  # the printed figures, not the true ones
    row["total"] = gt["rendered_total"]
    row["arithmetic_flag"] = gt["variants"]["consistency"] != "correct"
    return {f: "" if v is None else str(v).lower() if isinstance(v, bool) else str(v) for f, v in row.items()}


def matches(field, exp, got):
    exp, got = exp.strip(), got.strip()
    if field in AMOUNT_FIELDS or field == "vat_rate":
        if not exp or not got:
            return exp == got
        try:
            tol = Decimal("0.01") if field in AMOUNT_FIELDS else Decimal("0.001")
            return abs(Decimal(exp) - Decimal(got)) <= tol
        except InvalidOperation:
            return False
    if field in BOOL_FIELDS:
        return exp.lower() == got.lower()
    norm = lambda s: " ".join(unicodedata.normalize("NFC", s).split())
    return norm(exp) == norm(got)


def pct(correct, n):
    return f"{100 * correct / n:.1f}%" if n else "-"


def main(csv_path):
    name = Path(csv_path).stem.split("_")[0]
    with open(csv_path, newline="", encoding="utf-8") as f:
        got = {r["invoice_id"]: r for r in csv.DictReader(f)}
    gts = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data" / "ground_truth").glob("*.json"))]

    errors = []
    ok = {}  # (invoice_id, field) -> bool
    for gt in gts:
        inv, exp = gt["invoice_id"], expected_row(gt)
        for f in COMPARED:
            g = got.get(inv, {}).get(f) or ""  # a missing row counts as all fields wrong/empty
            ok[inv, f] = inv in got and matches(f, exp[f], g)
            if not ok[inv, f]:
                errors.append([inv, f, exp[f], g if inv in got else "<missing row>"]
                              + [gt["variants"][k] for k in VARIANT_KEYS])

    def acc(invoices, fields):
        cells = [ok[i, f] for i in invoices for f in fields]
        return sum(cells), len(cells)

    all_ids = [gt["invoice_id"] for gt in gts]
    perfect = sum(all(ok[i, f] for f in COMPARED) for i in all_ids)
    md = [f"# Evaluation: {Path(csv_path).name}", "",
          f"- Invoices: {len(all_ids)} in ground truth, {len(got)} in CSV, {len(set(all_ids) - set(got))} missing",
          f"- All fields: {pct(*acc(all_ids, COMPARED))} ({acc(all_ids, COMPARED)[0]}/{acc(all_ids, COMPARED)[1]} cells)",
          f"- Invoices with every field correct: {perfect}/{len(all_ids)}", "",
          "## Accuracy per field", "", "| Field | Correct | Accuracy |", "|---|---|---|"]
    for f in COMPARED:
        c, n = acc(all_ids, [f])
        md.append(f"| {f} | {c}/{n} | {pct(c, n)} |")

    for key in VARIANT_KEYS:
        groups = defaultdict(list)
        for gt in gts:
            groups[gt["variants"][key]].append(gt["invoice_id"])
        md += ["", f"## Accuracy by {key}", "",
               f"| {key} | n | all fields | " + " | ".join(COMPARED) + " |",
               "|---" * (len(COMPARED) + 3) + "|"]
        for value, ids in sorted(groups.items()):
            md.append(f"| {value} | {len(ids)} | {pct(*acc(ids, COMPARED))} | "
                      + " | ".join(pct(*acc(ids, [f])) for f in COMPARED) + " |")

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    (out / f"{name}_eval.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    with open(out / f"{name}_errors.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["invoice_id", "field", "expected", "got"] + VARIANT_KEYS)
        w.writerows(errors)
    print(f"wrote {out / f'{name}_eval.md'} and {out / f'{name}_errors.csv'} ({len(errors)} errors)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
