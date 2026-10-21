LEGAL INTELLIGENCE — REVIEW DASHBOARD
=====================================
1. Back up: Copy-Item app\frontend\streamlit_app.py app\frontend\streamlit_app.py.bak
2. Extract this ZIP at C:\Users\DIKSHA\legal-intelligence (preserve app/frontend folders).
3. Terminal 1: python -m uvicorn app.main:app --port 8000
4. Terminal 2: python -m streamlit run app/frontend/streamlit_app.py
5. Open http://localhost:8501
6. Select Fast review for live presentation. Choose Full analysis only to demonstrate M3 summarization + M4 translation.
7. Save local history only with permission. It stores findings in data/review_dashboard/history.sqlite3 (not PDF bytes).
8. Run M9 test: python -m evaluation.evaluate_m9

NOTES
- No changes to your existing FastAPI or AI model code.
- Fast review calls M1, M2, M5, M6, M7. M3/M4 only run in Full analysis; M8/M9 have dedicated tabs.
- M2's 82.5% is the keyword baseline on 40 synthetic employment clauses, not full hybrid/four-domain accuracy.
- Research metrics shown are historical development results; rerun evaluations before final paper.
- No new law monitoring is added by this dashboard. Existing indexed legal documents are searchable under M8.
- First use may be slow as your AI modules load; keep the backend running before the review.
- Full mode can take minutes on CPU for large PDFs. Fast mode is faster but has no summary/translation.
