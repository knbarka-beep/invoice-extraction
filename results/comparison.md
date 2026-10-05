# Comparison of methods 1 to 4

Raw material for the report. All figures come from `evaluate.py` run on the four CSVs in `outputs/` (50 invoices, 14 compared fields, 700 cells per method).

| Method | What it is |
|---|---|
| 1 Rules | pdfplumber text + regex and rules, no LLM |
| 2 Gemini | Gemini flash-lite does the whole extraction from one shared prompt |
| 3 Claude Opus | Claude Opus 5.5 does the whole extraction from the same prompt |
| 4 Hybrid | Gemini flash-lite only transcribes what is printed; Python parses numbers, derives VAT and sets the arithmetic flag. Figures below are from the second run (see "Method 4: two runs") |

## Accuracy per field

| Field | 1 Rules | 2 Gemini | 3 Claude Opus | 4 Hybrid |
|---|---|---|---|---|
| vendor | 50/50 | 50/50 | 50/50 | 50/50 |
| vendor_country | 50/50 | 50/50 | 50/50 | 50/50 |
| recipient | 50/50 | 50/50 | 50/50 | 50/50 |
| recipient_country | 50/50 | 50/50 | 50/50 | 50/50 |
| date | 50/50 | 50/50 | 50/50 | 50/50 |
| due_date | 50/50 | 50/50 | 50/50 | 50/50 |
| currency | 50/50 | 50/50 | 50/50 | 50/50 |
| subtotal | 47/50 | 44/50 | 47/50 | 47/50 |
| vat_rate | 47/50 | 48/50 | 47/50 | 47/50 |
| vat_amount | 47/50 | 45/50 | 47/50 | 47/50 |
| discount_amount | 50/50 | 49/50 | 50/50 | 50/50 |
| total | 50/50 | 50/50 | 50/50 | 50/50 |
| is_credit_note | 50/50 | 50/50 | 50/50 | 50/50 |
| arithmetic_flag | 50/50 | 35/50 | 50/50 | 50/50 |
| **All cells** | 691/700 (98.7%) | 671/700 (95.9%) | 691/700 (98.7%) | 691/700 (98.7%) |
| **Invoices fully correct** | 47/50 | 30/50 | 47/50 | 47/50 |

## Accuracy by variant

Share of cells correct (all 14 fields) for the invoices with that variant value; n is the number of invoices.

| Variant key | Value | n | 1 Rules | 2 Gemini | 3 Claude Opus | 4 Hybrid |
|---|---|---|---|---|---|---|
| vat_variant | explicit_excluded | 12 | 100.0% | 98.2% | 100.0% | 100.0% |
| vat_variant | explicit_included | 10 | 93.6% | 88.6% | 93.6% | 93.6% |
| vat_variant | implicit_no_rate | 15 | 100.0% | 97.1% | 100.0% | 100.0% |
| vat_variant | implicit_rate_stated | 13 | 100.0% | 97.8% | 100.0% | 100.0% |
| discount_variant | explicit_amount | 6 | 100.0% | 95.2% | 100.0% | 100.0% |
| discount_variant | explicit_percentage | 8 | 100.0% | 96.4% | 100.0% | 100.0% |
| discount_variant | none | 21 | 96.9% | 95.6% | 96.9% | 96.9% |
| discount_variant | obfuscated | 7 | 100.0% | 95.9% | 100.0% | 100.0% |
| discount_variant | trade_terms | 8 | 100.0% | 96.4% | 100.0% | 100.0% |
| number_format | english | 13 | 100.0% | 96.7% | 100.0% | 100.0% |
| number_format | german | 19 | 98.9% | 94.4% | 98.9% | 98.9% |
| number_format | swiss | 18 | 97.6% | 96.8% | 97.6% | 97.6% |
| consistency | correct | 28 | 98.5% | 96.2% | 98.5% | 98.5% |
| consistency | subtotal_error | 11 | 98.1% | 91.6% | 98.1% | 98.1% |
| consistency | total_error | 11 | 100.0% | 99.4% | 100.0% | 100.0% |
| edge_case | credit_note | 2 | 100.0% | 100.0% | 100.0% | 100.0% |
| edge_case | mixed_vat | 1 | 100.0% | 100.0% | 100.0% | 100.0% |
| edge_case | none | 43 | 98.5% | 95.5% | 98.5% | 98.5% |
| edge_case | reverse_charge | 1 | 100.0% | 100.0% | 100.0% | 100.0% |
| edge_case | single_item | 3 | 100.0% | 95.2% | 100.0% | 100.0% |

## Errors shared by every method

INV-2026-0015, 0029 and 0034 fail on subtotal, vat_rate and vat_amount in all four methods (9 cells each for methods 1, 3 and 4). They print "The subtotal including VAT is X" with no VAT rate and no VAT amount, while the ground truth assumes 20%. The rate is not on the invoice, so it can be neither transcribed nor derived.

- Methods 1 and 4 output the printed gross subtotal and leave vat_rate and vat_amount empty.
- Method 3 leaves all three empty.
- Method 2 guessed (see the next section).

## Cases where an LLM changed a printed figure

Method 3 (Claude Opus): none.

Method 2 (Gemini, whole extraction):

| Invoice | Field | Expected | Got | What happened |
|---|---|---|---|---|
| INV-2026-0013 | subtotal | 15733.90 | 15743.90 | Replaced the wrong printed subtotal with the arithmetically correct one (total / 1.2) |
| INV-2026-0015 | discount_amount | 0.00 | 10.00 | Invented a discount equal to the gap between printed subtotal and total; arithmetic_flag then set to false |
| INV-2026-0015 | subtotal, vat_amount | 133275.50, 26653.10 | 133273.83, 26654.77 | Assumed 20% although no rate is printed; took printed gross subtotal / 1.2 |
| INV-2026-0029 | vat_rate, vat_amount | 0.20, 1479.60 | 0.00, 0.00 | Invented a zero rate where none is printed; subtotal left gross |
| INV-2026-0006 | subtotal, vat_amount | 12923.70, 2583.74 | 12922.87, 2584.57 | Net derived as printed gross subtotal / 1.2 instead of gross minus line-item VAT |
| INV-2026-0018 | subtotal, vat_amount | 191172.20, 38244.44 | 191180.53, 38236.11 | Same derivation as INV-2026-0006 |

The last two rows are a different derivation from a printed figure, not an altered printed figure; they differ from the ground truth only because those invoices carry a subtotal error.

Method 2's other errors are judgement, not changed figures: arithmetic_flag is wrong on 15 invoices (9 false alarms on consistent invoices, 6 missed errors).

Method 4 (Gemini, transcription only): no altered amount in either run. The first run had one transcription error:

| Invoice | Run | Field | Expected | Got | What happened |
|---|---|---|---|---|---|
| INV-2026-0038 | first | vat_rate | 0.20 | 0.05 | The invoice prints no VAT rate; the output matches the "5%" of the early payment discount having been transcribed as a VAT percentage, which Python then used instead of deriving the rate from VAT amount / subtotal. The raw transcription of the first run was not saved, so this is inferred from the output. |

## Method 4: two runs

| | First run | Second run |
|---|---|---|
| All cells | 690/700 (98.6%) | 691/700 (98.7%) |
| Invoices fully correct | 46/50 | 47/50 |
| vat_rate | 46/50 | 47/50 |
| Errors beyond INV-2026-0015, 0029, 0034 | INV-2026-0038 vat_rate | none |
| Reconciliation check | not present | present, triggered on 0 invoices |

- After the first run, prompted by the INV-2026-0038 error, a reconciliation check was added to the Python step: when a VAT amount and a net subtotal are both available and a transcribed VAT rate differs from VAT amount / subtotal by more than 0.005, the computed ratio is used and the override is logged in the `vat_rate_override` column of `results/method4_usage.csv`. The check runs on every invoice. Because it was added after seeing an evaluation result, it is a change tuned on the test set.
- All 50 invoices were then run again (new LLM calls). The check did not trigger on any invoice in the second run: this time Gemini transcribed INV-2026-0038 with an empty list of VAT percentages (`results/method4_raw/INV-2026-0038.json`), so the rate was derived as before and came out right. The one-cell improvement between the runs therefore comes from run-to-run variation in the LLM's transcription, not from the check. The check is a safeguard that would have corrected the first run's error.
- The second run also saves every raw transcription to `results/method4_raw/<invoice_id>.json`.
- The committed `outputs/method4_hybrid.csv` and `results/method4_*` files are the second run; the first run's files are in git commit `05ff2bb`.

## Token use and run time

| | 2 Gemini | 3 Claude Opus | 4 Hybrid |
|---|---|---|---|
| Model | gemini-3.1-flash-lite-preview (37 calls), gemini-flash-lite-latest (13 calls) | claude-opus-5-5 (50 calls) | gemini-3.1-flash-lite-preview (50 calls) |
| Input tokens | 44,388 | 80,427 | 39,788 |
| Output tokens | 10,256 | 21,639 | 24,843 |
| Run time | 727 s (12 min) | 305 s (5 min) | 1,139 s (19 min) |
| Failed calls | 0 | 0 | 0 |
| Cost | Gemini free tier | Claude Pro subscription; API-equivalent $1.08 | Gemini free tier |

Notes:

- Method 2: 13 of the 50 calls went to the fallback model gemini-flash-lite-latest after a 503 or 429 from gemini-3.1-flash-lite-preview, so method 2 is a mix of two models.
- Method 4 is one model throughout. It retries the same model with backoff instead of falling back, which is why it ran longer. A probe during the run returned 503 UNAVAILABLE ("This model is currently experiencing high demand"), i.e. server overload, not a 429 quota limit; the errors retried during the run itself were not logged.
- Method 4 figures in this table are the second run. Its run time includes 66 s for two calls (INV-2026-0001 and 0002) that failed when the internet connection dropped; they were retried with the same model and succeeded, and are not counted as failed calls in the final output. The first run used 39,788 input / 24,856 output tokens and took 1,020 s (17 min).
- Gemini run times include a 5 s pause after every call.
- Method 3 input tokens include about 580 tokens per call that the Claude Code CLI adds and caches on top of the prompt. The cost is the CLI's reported `total_cost_usd`, an API-equivalent figure, not money paid.
- Method 4 uses more output tokens than method 2 because it transcribes every line item.
