# Evaluation: method2_gemini.csv

- Invoices: 50 in ground truth, 50 in CSV, 0 missing
- All fields: 95.9% (671/700 cells)
- Invoices with every field correct: 30/50

## Accuracy per field

| Field | Correct | Accuracy |
|---|---|---|
| vendor | 50/50 | 100.0% |
| vendor_country | 50/50 | 100.0% |
| recipient | 50/50 | 100.0% |
| recipient_country | 50/50 | 100.0% |
| date | 50/50 | 100.0% |
| due_date | 50/50 | 100.0% |
| currency | 50/50 | 100.0% |
| subtotal | 44/50 | 88.0% |
| vat_rate | 48/50 | 96.0% |
| vat_amount | 45/50 | 90.0% |
| discount_amount | 49/50 | 98.0% |
| total | 50/50 | 100.0% |
| is_credit_note | 50/50 | 100.0% |
| arithmetic_flag | 35/50 | 70.0% |

## Accuracy by vat_variant

| vat_variant | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| explicit_excluded | 12 | 98.2% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 75.0% |
| explicit_included | 10 | 88.6% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 40.0% | 80.0% | 50.0% | 90.0% | 100.0% | 100.0% | 80.0% |
| implicit_no_rate | 15 | 97.1% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 60.0% |
| implicit_rate_stated | 13 | 97.8% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 69.2% |

## Accuracy by discount_variant

| discount_variant | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| explicit_amount | 6 | 95.2% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 33.3% |
| explicit_percentage | 8 | 96.4% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 87.5% | 100.0% | 87.5% | 100.0% | 100.0% | 100.0% | 75.0% |
| none | 21 | 95.6% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 81.0% | 90.5% | 85.7% | 95.2% | 100.0% | 100.0% | 85.7% |
| obfuscated | 7 | 95.9% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 42.9% |
| trade_terms | 8 | 96.4% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 87.5% | 100.0% | 87.5% | 100.0% | 100.0% | 100.0% | 75.0% |

## Accuracy by number_format

| number_format | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| english | 13 | 96.7% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 84.6% | 100.0% | 84.6% | 100.0% | 100.0% | 100.0% | 84.6% |
| german | 19 | 94.4% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 89.5% | 100.0% | 94.7% | 94.7% | 100.0% | 100.0% | 42.1% |
| swiss | 18 | 96.8% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 88.9% | 88.9% | 88.9% | 100.0% | 100.0% | 100.0% | 88.9% |

## Accuracy by layout

| layout | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mixed | 15 | 92.9% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 80.0% | 86.7% | 80.0% | 93.3% | 100.0% | 100.0% | 60.0% |
| paragraph | 16 | 96.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 87.5% | 100.0% | 93.8% | 100.0% | 100.0% | 100.0% | 62.5% |
| table | 19 | 98.1% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 94.7% | 100.0% | 94.7% | 100.0% | 100.0% | 100.0% | 84.2% |

## Accuracy by consistency

| consistency | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| correct | 28 | 96.2% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 92.9% | 92.9% | 92.9% | 100.0% | 100.0% | 100.0% | 67.9% |
| subtotal_error | 11 | 91.6% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 63.6% | 100.0% | 72.7% | 90.9% | 100.0% | 100.0% | 54.5% |
| total_error | 11 | 99.4% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 90.9% |

## Accuracy by edge_case

| edge_case | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| credit_note | 2 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| mixed_vat | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| none | 43 | 95.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 86.0% | 95.3% | 88.4% | 97.7% | 100.0% | 100.0% | 69.8% |
| reverse_charge | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| single_item | 3 | 95.2% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 33.3% |
