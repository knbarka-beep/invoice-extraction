# Error types by method

Number of invoices affected (of 50). Built from `results/method1..4_errors.csv`, the first method 4 run's errors CSV in commit `05ff2bb`, and the output CSVs. An invoice can appear in more than one row.

| Error type | 1 Rules | 2 Gemini | 3 Claude Opus | 4 Hybrid, first run | 4 Hybrid, second run |
|---|---|---|---|---|---|
| VAT rate and amount missing because the invoice prints neither | 3 | 1 | 3 | 3 | 3 |
| arithmetic_flag false alarm (consistent invoice flagged) | 0 | 9 | 0 | 0 | 0 |
| arithmetic_flag miss (inconsistent invoice not flagged) | 0 | 6 | 0 | 0 | 0 |
| Printed figure silently corrected | 0 | 1 | 0 | 0 | 0 |
| Figure invented to make the arithmetic work | 0 | 1 | 0 | 0 | 0 |
| VAT derived from gross with an assumed rate | 0 | 1 | 0 | 0 | 0 |
| Zero VAT rate and amount invented where none is printed | 0 | 1 | 0 | 0 | 0 |
| Net and VAT taken as printed gross subtotal / 1.2 instead of from the line items (rate is printed) | 0 | 2 | 0 | 0 | 0 |
| Discount percentage read as VAT rate | 0 | 0 | 0 | 1 | 0 |

| | 1 Rules | 2 Gemini | 3 Claude Opus | 4 Hybrid, first run | 4 Hybrid, second run |
|---|---|---|---|---|---|
| Affected cells (of 700) | 9 | 29 | 9 | 10 | 9 |
| Invoices with any error | 3 | 20 | 3 | 4 | 3 |

Which invoices, and cells per type:

- **VAT rate and amount missing** (3 cells per invoice: subtotal, vat_rate, vat_amount): INV-2026-0015, 0029, 0034 for methods 1, 3 and 4; only 0034 for method 2. Methods 1, 2 and 4 output the printed gross subtotal; method 3 leaves the subtotal empty.
- **False alarms** (9 cells): INV-2026-0005, 0007, 0022, 0023, 0027, 0031, 0042, 0046, 0048.
- **Misses** (6 cells): INV-2026-0012, 0015, 0021, 0024, 0032, 0047.
- **Silently corrected** (1 cell): INV-2026-0013, subtotal 15743.90 (= printed total / 1.2) instead of 15733.90.
- **Invented figure** (1 cell): INV-2026-0015, discount 10.00, the gap between printed subtotal and total.
- **Assumed rate** (2 cells): INV-2026-0015, subtotal and vat_amount from printed gross subtotal / 1.2 although no rate is printed.
- **Zero VAT invented** (3 cells): INV-2026-0029, vat_rate 0.00 and vat_amount 0.00, subtotal left gross.
- **Gross / 1.2** (4 cells): INV-2026-0006 and 0018, subtotal and vat_amount; wrong only because these invoices carry a subtotal error.
- **Discount percentage as VAT rate** (1 cell): INV-2026-0038, vat_rate 0.05.

Limits: raw replies were saved only for the second method 4 run. Method 2's types are read from its output values (each stated derivation reproduces the output to the cent); the method 4 first-run type is inferred from the output value 0.05 matching the invoice's 5% discount.
