# Legal Intelligence — immediate 6-priority execution

This package **does not** create four-domain accuracy from four example PDFs. It provides a real API smoke test and latency evidence. For scientific accuracy, use independently labeled held-out clauses and documents in the prior four-domain evaluation kit.

## Install
1. Back up `app/modules/m9_comparison/agreement_comparator.py` before replacing it.
2. Copy this ZIP's `app` and `evaluation` folders into your existing project root, preserving other files.
3. `pip install requests` if missing.
4. Start backend: `python -m uvicorn app.main:app --port 8000`.

## 1. Four-domain PDF smoke test + end-to-end latency
Use four actual PDFs (ideally with no private personal data). Example:

```powershell
python -m evaluation.run_four_pdf_review --employment "samples\employment.pdf" --rental "samples\rental.pdf" --property "samples\property.pdf" --divorce "samples\divorce.pdf" --mode fast
```

Then full analysis on short documents:

```powershell
python -m evaluation.run_four_pdf_review --employment "samples\employment.pdf" --rental "samples\rental.pdf" --property "samples\property.pdf" --divorce "samples\divorce.pdf" --mode full --language Marathi
```

Results: `evaluation/results/four_pdf_review/*.json` and `fast_results.csv` / `full_results.csv`. Fast mode is only M1+M2 on your current API, NOT M1+M2+M5+M6+M7. Full mode runs M1–M7. The `--mode full` call supplies the expected category as a hint, so it cannot be used to claim category-detection accuracy. The script saves potentially sensitive analysis text in JSON locally: do not commit those files.

## 2. M9 comparison fix and retest
Replacement comparator uses one-to-one clause matching and flags changed wording/numbers. Run:

```powershell
python -m evaluation.evaluate_m9
```

Inspect **actual** `changed_clauses` for the two expected changes. `evaluate_m9.py` currently estimates detected changes by count, which can produce misleading results; do not report F1 until changes are independently matched to ground truth.

## 3. Multilingual validation
Full-mode outputs `employment_full.json`, etc. Check `summary` and `translated_summary` for factual consistency, correct numbers, dates, obligations, and readable Hindi/Marathi. Check both languages. Use independently reviewed references for BLEU/chrF.

## 4. Timing
Compare CSV `seconds` for fast vs full. For a latency distribution repeat on a representative document sample (e.g. 10+ files per domain), report p50/p95, warm/cold separately. Do not call the single 4-PDF average a benchmark of general latency.

## 5. Paper
Existing M2: keyword 82.50%, semantic 87.50%, hybrid 87.50% on 40 **synthetic employment** clauses; hybrid macro-F1 86.81%. Do not claim these scores for rental/property/divorce. Other module results from earlier evaluation logs are preliminary. Four-domain test labels must be independently reviewed.

## 6. Website
Run `python -m streamlit run app/frontend/streamlit_app.py`; demonstrate one fast and one full result, save history and download report. Verify each screen and report before screenshots. Do not display fake sample results as measured output.

## Deployment and privacy
Do not commit uploaded PDFs, saved analyses, SQLite DB, secrets, `.env`, `.venv`, or user PII to GitHub. Streamlit local SQLite is not a multi-user production storage design; add authentication and persistent storage before public deployment.
