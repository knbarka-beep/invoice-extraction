# Evaluation: method4_hybrid.csv

- Invoices: 50 in ground truth, 50 in CSV, 0 missing
- All fields: 98.6% (690/700 cells)
- Invoices with every field correct: 46/50

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
| subtotal | 47/50 | 94.0% |
| vat_rate | 46/50 | 92.0% |
| vat_amount | 47/50 | 94.0% |
| discount_amount | 50/50 | 100.0% |
| total | 50/50 | 100.0% |
| is_credit_note | 50/50 | 100.0% |
| arithmetic_flag | 50/50 | 100.0% |

## Accuracy by vat_variant

| vat_variant | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| explicit_excluded | 12 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| explicit_included | 10 | 93.6% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 70.0% | 70.0% | 70.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| implicit_no_rate | 15 | 99.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 93.3% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| implicit_rate_stated | 13 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

## Accuracy by discount_variant

| discount_variant | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| explicit_amount | 6 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| explicit_percentage | 8 | 99.1% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 87.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| none | 21 | 96.9% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 85.7% | 85.7% | 85.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| obfuscated | 7 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| trade_terms | 8 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

## Accuracy by number_format

| number_format | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| english | 13 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| german | 19 | 98.9% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 94.7% | 94.7% | 94.7% | 100.0% | 100.0% | 100.0% | 100.0% |
| swiss | 18 | 97.2% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 88.9% | 83.3% | 88.9% | 100.0% | 100.0% | 100.0% | 100.0% |

## Accuracy by layout

| layout | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| mixed | 15 | 95.7% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 80.0% | 80.0% | 80.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| paragraph | 16 | 99.6% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 93.8% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| table | 19 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

## Accuracy by consistency

| consistency | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| correct | 28 | 98.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 92.9% | 92.9% | 92.9% | 100.0% | 100.0% | 100.0% | 100.0% |
| subtotal_error | 11 | 98.1% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 90.9% | 90.9% | 90.9% | 100.0% | 100.0% | 100.0% | 100.0% |
| total_error | 11 | 99.4% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 90.9% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |

## Accuracy by edge_case

| edge_case | n | all fields | vendor | vendor_country | recipient | recipient_country | date | due_date | currency | subtotal | vat_rate | vat_amount | discount_amount | total | is_credit_note | arithmetic_flag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| credit_note | 2 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| mixed_vat | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| none | 43 | 98.3% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 93.0% | 90.7% | 93.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| reverse_charge | 1 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| single_item | 3 | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
