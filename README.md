# Invoice extraction

Extract 50 invoices (`data/pdf`) into CSV with four methods and compare each against `data/ground_truth`. See `ASSIGNMENT_REQUIREMENTS.md`.

| Method | File | Status |
|---|---|---|
| 1. Rules (pdfplumber + regex, no LLM) | `methods/method1_rules.py` | done |
| 2. Low-cost LLM (Gemini flash-lite, free tier) | `methods/method2_gemini.py` | done |
| 3. Expensive LLM (Claude Opus via Claude Code CLI) | `methods/method3_claude.py` | done |
| 4. Refined: hybrid (Gemini flash-lite transcribes, Python computes) | `methods/method4_hybrid.py` | done |

## Setup

```
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
```

## Run

```
py -m methods.method1_rules              # writes outputs/method1_rules.csv
py evaluate.py outputs/method1_rules.csv # writes results/method1_eval.md, results/method1_errors.csv
py -m methods.method2_gemini             # needs GEMINI_API_KEY=... in .env
py -m methods.method3_claude             # needs the `claude` CLI, logged in
py -m methods.method4_hybrid             # needs GEMINI_API_KEY=... in .env
```

Methods 2 and 3 share one prompt and run loop (`methods/llm_common.py`) and read the same pdfplumber text as method 1. Each writes `outputs/<method>.csv` and a per-invoice token log `results/<method>_usage.csv`. A failed call leaves an empty row with the error in the usage log; rerunning retries only the failed or missing invoices.

## Output schema

All methods write the same CSV, one row per invoice, defined in `schema.py`:

`invoice_id, vendor, vendor_country, recipient, recipient_country, date, due_date, currency, subtotal, vat_rate, vat_amount, discount_amount, total, is_credit_note, arithmetic_flag`

- Dates are ISO (`YYYY-MM-DD`), countries are ISO 3166 alpha-2, amounts are plain decimals with two places, `vat_rate` is a fraction (`0.20`).
- `subtotal` and `total` are the figures printed on the invoice, even when they are wrong. `subtotal` is net of VAT.
- `arithmetic_flag` is `true` when the printed figures do not add up.
- A value that cannot be determined is left empty.

## Evaluation

`evaluate.py` compares a method CSV field by field with the ground truth: `subtotal`/`total` against `rendered_subtotal`/`rendered_total`, `arithmetic_flag` against `variants.consistency != "correct"`, amounts within 0.01. It reports accuracy per field and per value of each `variants` key.

The four methods are compared in `results/comparison.md`.
