# Legal Saathi — Smart Completion Kit

This is a **non-destructive supplement** for the user's existing Legal Intelligence FastAPI project. It does not contain the full nine-module project or new trained models. It bundles the previously prepared Streamlit V2 UI and adds repeatable M2 comparison and API benchmark scripts.

## Windows PowerShell, from project root

```powershell
cd C:\Users\DIKSHA\legal-intelligence
# First BACK UP any file you will overwrite
Copy-Item app\frontend\streamlit_app.py app\frontend\streamlit_app.py.bak -ErrorAction SilentlyContinue
# Extract this ZIP into project root, preserving folders
pip install streamlit requests pandas scikit-learn
python -m evaluation.evaluate_m2_comparison
# In terminal 1
python -m uvicorn app.main:app --port 8000
# In terminal 2
python -m streamlit run app/frontend/streamlit_app.py
# In terminal 3, use a real PDF path:
python -m evaluation.benchmark_api --pdf "path\to\employment.pdf" --mode fast --runs 3
```

**Critical caveat:** The UI's 'Fast Review' calls M1, M2, M5, M6, M7 sequentially and is distinct from the benchmark script's `/api/analyze-pdf` endpoint, which tests M1+M2 only. Do not equate those times. The UI's local SQLite history is a prototype, **not secure multi-user cloud storage**. Do not deploy it with sensitive user documents until authentication, authorization, encryption, retention/deletion controls and persistent cloud database are in place.

## Fast completion order

1. Confirm four-domain category detection and each domain-specific rule with **one real sample each**; inspect failure cases.
2. Run M9 test: `python -m evaluation.evaluate_m9` (after installing corrected comparator); do not claim fix until 2/2 detected with correct matching.
3. Run `python -m evaluation.evaluate_m2_comparison`; inspect confusion matrices and ensure hybrid metrics actually improve before claiming it.
4. Run Fast Review on a 1–2 page text PDF and Full Analysis on one sample. Record processing time.
5. Test Hindi and Marathi generated outputs with a fluent reviewer. Confirm numbers, names, dates and legal meanings.
6. Capture screenshots of actual outputs and export a report.
7. Commit safe source code to GitHub; do not commit PDFs, `.env`, `.venv`, model caches or `history.sqlite3`.
8. Treat official-law monitoring and Google Cloud deployment as **pending** until implemented and verified. Avoid promising fully automatic retraining.

## For the IEEE paper

Use `docs/RESEARCH_EVIDENCE.md` as a source-limited preliminary results table. Final tables must be generated from reviewed held-out tests and measured timings. No claimed accuracy advantage over external websites without same-dataset benchmarking.
