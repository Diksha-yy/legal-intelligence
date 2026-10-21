# Legal Intelligence — 16-law starter collector

This starter contains the **16 rows reconstructed from the table pasted in chat**; it is not a modification of an uploaded workbook. None of the 16 laws has been verified for completeness, current legal effect, or amendment coverage.

## Windows quick start

Copy the folder to `C:\Users\DIKSHA\legal-intelligence\law-collector`, then in PowerShell:

```powershell
cd C:\Users\DIKSHA\legal-intelligence\law-collector
python -m pip install -r requirements.txt
python collector.py --input sources.xlsx
```

- **3 direct `.pdf` URLs** are attempted automatically, if reachable. Network restrictions, site errors, or malformed responses are logged.
- **13 India Code `/pdf-viewer/` URLs** are NOT direct PDF links. For each `manual_required` entry, open `source_page_url` in your browser, click Download, and save the file exactly as `downloads/<domain>/<document_id>.pdf` (example `downloads/divorce/DIV_001.pdf`). Run the same command again; the collector will validate the saved file.
- Check `collection_report.csv` for successes, failures, duplicate SHA-256 values, and OCR warnings.
- `sources_updated.xlsx` is generated; your original `sources.xlsx` is preserved.
- Once PDFs are available, run `python collector.py --input sources.xlsx --extract` to generate `processed/pages.jsonl`. Extraction is **page-wise**, not legal-section parsing. Scanned pages need OCR.

## Critical data-quality rules

1. The original `source_page_url` is kept for provenance. Direct PDF links go in `pdf_url`. For 3 existing direct links both fields are set to the same PDF URL until a parent publication page is identified.
2. The downloaded file's signature, page count, and hash are machine-checked. **This does not verify the legal text, the document's official title, consolidation date, legal effectiveness, or amendment completeness.** Human review is required before setting `verification_status=verified`.
3. Never infer commencement, repeal, or applicability from a filename or upload date. Leave dates blank and `legal_status=unknown` until checked.
4. Related rules, amendments, notifications, commencement orders, and older versions should be added as separate document rows tied to the parent `law_id`. Only verified legal material should be used for present-day legal conclusions.
5. `pages.jsonl` is a raw RAG input, **not** a labeled agreement-clause training dataset. Build M2 training data from reviewed agreements separately.
6. Download only from authorized official sources. The collector intentionally does not reverse-engineer viewer endpoints, evade CAPTCHAs, or scrape restricted content.

## Next iteration

Once `collection_report.csv` shows 16 readable PDFs, implement legal section parsing, date-aware RAG, amendment discovery and cross-document linkage, with expert review of legal status.
