"""FastAPI adapter for the existing legal_updates.core; no Streamlit dependency."""
import os
from fastapi import APIRouter, Depends, Header, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field
from app.legal_updates import core

router = APIRouter(prefix="/api/legal-updates", tags=["Official Legal Updates"])


def require_admin(x_admin_key: str | None = Header(default=None)):
    expected = os.getenv("LEGAL_UPDATES_ADMIN_KEY", "")
    if not expected or not x_admin_key or x_admin_key != expected:
        raise HTTPException(status_code=403, detail="Admin access required")


class Decision(BaseModel):
    approve: bool
    reviewer: str = Field(min_length=2, max_length=120)
    notes: str = Field(min_length=5, max_length=3000)
    publication_date: str = ""
    effective_date: str = ""
    law_status: str = ""
    applicable_jurisdiction: str = ""


@router.get("/health")
def health():
    return {"status": "ok", "service": "legal-updates"}


@router.get("/sources")
def sources():
    result = core.list_sources()
    return [{"id": x["id"], "title": x["title"], "domain": x["domain"],
             "jurisdiction": x["jurisdiction"], "url": x["url"],
             "enabled": bool(x["enabled"])} for x in result]


@router.get("/reviews")
def reviews(status: str | None = Query(default=None, pattern="^(pending|approved|rejected)$"),
            limit: int = Query(default=50, ge=1, le=200)):
    result = core.reviews()
    if status:
        result = [r for r in result if r["status"] == status]
    # Never expose local filesystem paths or reviewer identity on public API.
    allowed = ("id", "source_id", "old_version", "new_version", "detected_at",
               "status", "publication_date", "effective_date", "law_status",
               "applicable_jurisdiction", "title", "url", "domain", "jurisdiction")
    return [{k: r.get(k) for k in allowed} for r in result[:limit]]


@router.get("/search")
async def search(q: str = Query(min_length=3, max_length=500),
                 domain: str | None = Query(default=None, max_length=40),
                 k: int = Query(default=5, ge=1, le=10)):
    # FAISS and embedding initialization are blocking CPU work.
    return await run_in_threadpool(core.search_approved, q, k, domain)


@router.post("/fetch-all", dependencies=[Depends(require_admin)])
async def fetch_all():
    # Intended for server-side operator / scheduler, never browser public access.
    return await run_in_threadpool(core.fetch_all)


@router.post("/fetch/{source_id}", dependencies=[Depends(require_admin)])
async def fetch_one(source_id: str):
    try:
        return await run_in_threadpool(core.fetch, source_id)
    except KeyError:
        raise HTTPException(404, "Source not found")
    except Exception as exc:
        raise HTTPException(502, f"Source fetch failed: {type(exc).__name__}")


@router.post("/reviews/{review_id}/decision", dependencies=[Depends(require_admin)])
async def decide(review_id: int, payload: Decision):
    try:
        return await run_in_threadpool(
            core.review_decision, review_id, payload.approve, payload.reviewer,
            payload.notes, payload.publication_date, payload.effective_date,
            payload.law_status, payload.applicable_jurisdiction
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc))


@router.post("/reviews/{review_id}/activate", dependencies=[Depends(require_admin)])
async def activate(review_id: int):
    try:
        return await run_in_threadpool(core.activate, review_id)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
