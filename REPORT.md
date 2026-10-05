# Invoice extraction: report

## Mistakes by method

All four methods read the same pdfplumber text and were scored field by field against the ground truth, 14 fields per invoice. The rules-based method and Claude Opus each got 691 of 700 cells right, and both failed only on the three invoices that print a VAT-inclusive subtotal but neither a VAT rate nor a VAT amount. Both left those fields empty. The ground truth assumes 20 %, but that figure is not on the document, so I treat this as a correct refusal rather than a weakness. The rules score is optimistic, though. The rules were written with all 50 invoices visible and there is no held-out set, so a new layout would likely break them. Gemini Flash-Lite on its own was much weaker at 671 cells. Most of its errors were in the arithmetic check, with nine false alarms and six missed errors. More worrying, it changed figures to make the arithmetic work. It replaced a wrong printed subtotal with the correct one, and it invented a 10 euro discount to close a gap and then reported the invoice as consistent. In 13 of its 50 calls the main model was overloaded and the fallback, which Google AI Studio shows as Gemini 3.5 Flash-Lite, answered instead. The refined method uses the same cheap model only to transcribe printed figures, and Python does all the arithmetic. This took Gemini from 30 to 47 fully correct invoices and removed every changed or invented figure. Its first run read a 5 % early payment discount as the VAT rate, so I added a check that compares the transcribed rate with VAT amount divided by subtotal. The check is unit tested but never triggered in the final run, where the error did not recur. The last point gained is therefore run-to-run variation in the model, not the check.

| Error type (invoices affected) | 1 Rules | 2 Gemini | 3 Claude Opus | 4 Hybrid (run 1 / run 2) |
|---|---|---|---|---|
| VAT rate and amount left empty, not printed on invoice | 3 | 1 | 3 | 3 / 3 |
| VAT rate guessed (20 % assumed or 0 % invented) | 0 | 2 | 0 | 0 / 0 |
| Net and VAT taken from gross ÷ 1,2 instead of line items | 0 | 2 | 0 | 0 / 0 |
| Printed figure silently corrected | 0 | 1 | 0 | 0 / 0 |
| Figure invented to make the arithmetic work | 0 | 1 | 0 | 0 / 0 |
| Arithmetic error flag: false alarm / miss | 0 / 0 | 9 / 6 | 0 / 0 | 0 / 0 |
| Discount percentage read as VAT rate | 0 | 0 | 0 | 1 / 0 |
| Cells wrong (of 700) | 9 | 29 | 9 | 10 / 9 |
| Invoices with any error (of 50) | 3 | 20 | 3 | 4 / 3 |

## Cost

The rules-based method has no API cost. Method 2 used Gemini 3.1 Flash-Lite on the free tier, with 44.388 input and 10.256 output tokens, so nothing was paid. The free tier has two catches. Google may use free-tier content to improve its products, which would rule it out for real supplier invoices, and there is no guaranteed capacity, so repeated "high demand" errors stretched the run to 12 minutes. Across all my Gemini runs that day, Google AI Studio shows a success rate of about 77 %, so roughly one request in four failed and had to be retried. Its output token total for the day closely matches the sum of my own logs. At the paid list price of $0,25 and $1,50 per million input and output tokens, the same run would have cost about $0,03. Method 3 called Claude Opus 5.5 through the Claude Code command line on my Claude Pro subscription, with 80.427 input and 21.639 output tokens. I paid nothing extra, but the run used part of the subscription's usage limit. Claude Code reports an API-equivalent cost of $1,08, about two cents per invoice and roughly 40 times the paid Gemini price, with no gain in accuracy over the free rules-based method. The refined method again ran on the Gemini free tier with 39.788 input and 24.843 output tokens, about $0,05 at the paid price. It produces more output tokens because it transcribes every line item, and it took 19 minutes, mostly waiting out overloaded servers.
