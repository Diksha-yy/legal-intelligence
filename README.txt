M9 SMART COMPARISON — INSTALLATION

1. Back up these existing files:
   app/services/legal_ai_pipeline.py
   app/services/multilingual_report.py
   app/modules/m9_comparison/comparison_engine.py (if present)

2. Copy the matching files from this ZIP into your existing project,
   preserving folders. Do not replace your entire app folder.

3. Run from project root:
   python -m py_compile app/services/legal_ai_pipeline.py
   python -m unittest discover -s tests -p test_m9.py
   python -m uvicorn app.main:app --port 8000

4. Existing /api/analyze-complete continues to run legal mode by default.
   The comparison_analysis field now has summary and important_findings.

5. Template and two_documents modes require reference_text (plain extracted text).
   Your current FastAPI endpoint does not expose comparison_mode/reference_text.
   To enable user uploads for those modes, add a separate API route to receive
   a second PDF, OCR it, then call run_comparison with mode='two_documents'.

6. M9 is an interpretable screening prototype, not validated legal compliance AI.
   Similarity matching can miss changes and falsely align clauses. Test it with
   verified examples before using accuracy claims in your IEEE paper.

7. M4 localization includes comparison_analysis, but original clause excerpts
   remain in source language and are not machine translated as evidence.
