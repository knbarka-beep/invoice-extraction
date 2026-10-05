# Log

| Date | Task | Time spent | Cost |
|---|---|---|---|
| 2026-10-05 | Setup, shared schema, method 1 (rules), evaluator | 20 min | no LLM API calls |
| 2026-10-05 | Method 2 (Gemini flash-lite), 50 invoices | 5 min (plus 12 min unattended run time) | Gemini free tier, 44,388 input / 10,256 output tokens |
| 2026-10-05 | Method 3 (Claude Opus 5.5), 50 invoices | 5 min (plus 5 min unattended run time) | Claude Pro subscription via Claude Code CLI, 80,427 input / 21,639 output tokens, API-equivalent $1.08 |
| 2026-10-05 | Method 4 (hybrid: Gemini flash-lite transcription + Python arithmetic), 50 invoices; comparison of methods 1-4 | 5 min (plus 17 min unattended run time) | Gemini free tier, 39,788 input / 24,856 output tokens |
| 2026-10-05 | Method 4 second run: VAT rate reconciliation check and raw transcriptions added, all 50 invoices rerun; comparison updated | 5 min (plus 19 min unattended run time) | Gemini free tier, 39,788 input / 24,843 output tokens |
| 2026-10-05 | Unit test for the method 4 reconciliation check; error type table (results/error_types.md) | 5 min | no LLM API calls |
