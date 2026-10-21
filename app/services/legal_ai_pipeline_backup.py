"""Legal Intelligence full-document pipeline (M1-M8).

Drop-in replacement for app/services/legal_ai_pipeline.py.
M9 remains a separate two-document comparison endpoint.
"""
from __future__ import annotations
from app.modules.m3_summarization.summarizer import summarize_text
from app.services.multilingual_report import localize_report
from app.modules.m4_translation.translator import translate_text

from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m2_classification.pipeline import analyze_document_clauses
from app.modules.m5_missing_clauses.missing_clause import detect_missing_clauses
from app.modules.m6_risk_scoring.risk_scorer import calculate_risk
from app.modules.m7_fairness.fairness_analyzer import analyze_fairness


DOMAIN_ALIASES = {
    "job_offer": "employment",
    "divorce_family": "divorce",
}
RAG_DOMAINS = {"rental", "employment", "divorce", "property"}


def retrieve_legal_references(document_text: str, domain: str, top_k: int = 5) -> dict:
    """Use the same cached FAISS model/index as /api/legal/search, without HTTP.

    This is supporting evidence retrieval, NOT legal validation or grounded risk scoring.
    """
    normalized_domain = DOMAIN_ALIASES.get(str(domain).lower(), str(domain).lower())
    if normalized_domain not in RAG_DOMAINS:
        return {
            "status": "skipped", "reason": f"Unsupported RAG domain: {domain}",
            "results": [], "count": 0,
        }

    try:
        from app.legal_search_router import load_retriever
        np, index, model, chunks = load_retriever()
        if index.ntotal == 0:
            return {"status": "unavailable", "reason": "FAISS index is empty", "results": [], "count": 0}

        # A short representative text query avoids embedding an entire lengthy PDF.
        # The domain is always included so the query has a meaningful context.
        query = f"{normalized_domain} agreement rights obligations legal requirements " + document_text[:900]
        vector = np.asarray(model.encode([query], normalize_embeddings=True), dtype="float32")
        scores, indices = index.search(vector, index.ntotal)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue
            chunk = chunks[int(idx)]
            if chunk.get("domain") != normalized_domain:
                continue
            results.append({
                "chunk_id": chunk.get("chunk_id"),
                "document_id": chunk.get("document_id"),
                "law_id": chunk.get("law_id"),
                "domain": chunk.get("domain"),
                "page": chunk.get("page"),
                "similarity": round(float(score), 4),
                "text": chunk.get("text", ""),
                "source_url": chunk.get("source_page_url"),
                "source_sha256": chunk.get("source_sha256"),
                "citation_granularity": "document_page",
                "verification_status": "unverified",
                "legal_status": chunk.get("legal_status", "unknown"),
            })
            if len(results) >= top_k:
                break

        return {
            "status": "retrieved", "domain": normalized_domain,
            "count": len(results), "results": results,
            "notice": "Experimental retrieval only. Verify current law and PDF pages before legal citation. Retrieval does not validate the risk assessment.",
        }
    except Exception as exc:
        # Retrieval failures must not erase otherwise successful M1-M7 analysis.
        return {
            "status": "unavailable", "reason": f"{type(exc).__name__}: {exc}",
            "count": 0, "results": [],
        }


def run_legal_ai_pipeline(pdf_path, target_language="Hindi", document_type=None):
    print("\n========== LEGAL AI PIPELINE START ==========", flush=True)

    print("[M1] OCR started", flush=True)
    ocr_result = extract_pdf_text(pdf_path)
    text = ocr_result["full_text"]
    if not text.strip():
        raise ValueError("No readable text found in PDF.")
    print("[M1] OCR completed", flush=True)

    print("[M2] Classification started", flush=True)
    classification = analyze_document_clauses(text, domain=document_type)
    if classification.get("error"):
        raise ValueError(classification["error"])
    domain = classification["domain"]
    # Domain used by existing document-analysis modules
    analysis_domain = {
        "divorce": "divorce_family"
    }.get(domain, domain)
    print("[M2] Classification completed", flush=True)

    # ==========================================
    # M3 - Optimized Summarization
    # ==========================================

    print("[M3] Summarization started", flush=True)

    summary_result = summarize_text(
        text,
        max_length=110,
        min_length=25,
        max_chunks=4
    )

    summary = summary_result["summary"]

    print("[M3] Summarization completed", flush=True)

    # ==========================================
    # M4 - Translation (Deferred)
    # ==========================================

    
    print("[M4] Translation delegated to report localization", flush=True)

    translated_summary = summary
    # ==========================================
    # M5 - Missing Clause Detection
    # ==========================================

    print("[M5] Missing clauses started", flush=True)

    missing_clauses = detect_missing_clauses(
        text,
        document_type=analysis_domain
    )

    print("[M5] Missing clauses completed", flush=True)

        # ==========================================
    # M6 - Risk Scoring
    # ==========================================

    print("[M6] Risk scoring started", flush=True)

    risk = calculate_risk(
        text,
        document_type=analysis_domain
    )

    print("[M6] Risk scoring completed", flush=True)

    # ==========================================
    # M7 - Fairness Analysis
    # ==========================================

    print("[M7] Fairness analysis started", flush=True)

    fairness = analyze_fairness(
        text,
        document_type=analysis_domain
    )

    print("[M7] Fairness analysis completed", flush=True)

    
    print("[M8] Legal RAG started", flush=True)
    legal_references = retrieve_legal_references(text, domain, top_k=5)
    print(f"[M8] Legal RAG {legal_references['status']}", flush=True)
    print("========== PIPELINE COMPLETED ==========", flush=True)

    report = {
        "status": "success",
        "document_type": domain,
        "ocr": {
            "filename": ocr_result["filename"],
            "page_count": ocr_result["page_count"],
            "text_length": len(text),
        },
        "classification": classification,
        "summary": summary,
        "translated_summary": translated_summary,
        "missing_clauses": missing_clauses,
        "risk_analysis": risk,
        "fairness_analysis": fairness,
        "legal_references": legal_references,
    }

   # ==========================================
    # Complete Multilingual Report
    # ==========================================

    print("[REPORT] Localization started", flush=True)

    report["localized_report"] = localize_report(
        report,
        target_language=target_language
    )

    report["report_language"] = target_language.strip().title()

    report["translated_summary"] = report["localized_report"]["summary"]

    print("[REPORT] Localization completed", flush=True)

    return report