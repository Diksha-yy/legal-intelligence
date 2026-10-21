# Legal Intelligence: official-source monitor + review-gated FAISS

## Installation (Windows PowerShell, from existing project root)
Copy `app/legal_updates/` and `scripts/legal_updates_cli.py` into your existing project; do NOT replace existing app modules.

```powershell
pip install pymupdf sentence-transformers faiss-cpu numpy streamlit
python -m scripts.legal_updates_cli register rera2016 "https://www.indiacode.nic.in/" property India "India Code landing page (DEMO; use direct official PDF URL instead)"
```

**Replace the demo landing-page URL with a direct, confirmed official PDF URL** from the source's website before fetching. Do not treat a website homepage as an Act. `robots.txt` restrictions are respected; blocked/unavailable sources should be manually downloaded in accordance with website terms, then ingested locally.

```powershell
python -m scripts.legal_updates_cli fetch rera2016
python -m scripts.legal_updates_cli reviews
```

The first snapshot is **not an amendment**. A changed content hash creates a pending review and unified diff. Site template changes can cause false positives.

To ingest a PDF you obtained from an official site:
```powershell
python -m scripts.legal_updates_cli ingest-local rera2016 "C:\path\to\official-act.pdf"
```

After independently checking official provenance, law status, jurisdiction, effective date and diff, approve:
```powershell
python -m scripts.legal_updates_cli decide 1 --approve --reviewer "Project Reviewer" --notes "Verified against official publication; baseline snapshot" --law-status "Act" --jurisdiction "India"
python -m scripts.legal_updates_cli activate 1
python -m scripts.legal_updates_cli search "What are the promoter obligations?"
```

Rejected review:
```powershell
python -m scripts.legal_updates_cli decide 2 --reviewer "Project Reviewer" --notes "Website layout changed, not a legal amendment"
```

## Streamlit integration
Add these two lines to your existing `app/frontend/streamlit_app.py` (in an appropriate tab/page):
```python
from app.legal_updates.streamlit_panel import render_legal_updates
render_legal_updates()
```
Run Streamlit from project root: `python -m streamlit run app/frontend/streamlit_app.py`.

## Integrating into M8
`from app.legal_updates import search_approved` then call `search_approved(question,k=5)` as a **separate, approved legal-update retrieval source**. Existing M8 knowledge base remains untouched. Merge results only after you inspect M8's interface, check citations and jurisdiction, and add tests. Approval does not guarantee legal correctness.

## Scheduler
Use Windows Task Scheduler to run `python -m scripts.legal_updates_cli fetch SOURCE_ID` daily for each configured official PDF URL. Scheduler only stages changes as pending. No automatic approval/retraining. Prefer official APIs/feeds where available.

## Limitations
- No CAPTCHA bypass, bulk scraping, or arbitrary user URLs. Source URLs are configured by a trusted operator, not public visitors.
- Source website permission and terms must be checked; robots.txt is a conservative technical gate, not a license.
- The fetched PDF must contain selectable text. Scanned PDFs need a separate OCR workflow.
- PDF byte hash detects changes including metadata-only changes; reviewer must inspect text diff.
- `activate` builds an independent approved FAISS index; it **does not** silently overwrite the existing M8 index.
- Not an automated law-validity determination. Dates and jurisdiction require human verification.
- Streamlit panel is read-only to prevent unauthenticated users approving legal updates.
- For a real deployment, add authentication, rate limits, audit logging, source allowlist, secure storage and independent RAG regression tests before automatic index promotion.
