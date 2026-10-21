
import os
from app.legal_search_router import router as legal_search_router
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Existing AI modules
from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m2_classification.classifier import classify_document
from app.modules.m5_missing_clauses.missing_clause import (
    detect_missing_clauses
)
from app.modules.m6_risk_scoring.risk_scorer import calculate_risk
from app.modules.m7_fairness.fairness_analyzer import analyze_fairness
from app.modules.m8_rag.legal_qa import LegalQA
from app.modules.m9_comparison.agreement_comparator import (
    AgreementComparator
)


from app.services.legal_ai_pipeline_backup import run_legal_ai_pipeline
from fastapi import UploadFile, File, HTTPException
from tempfile import TemporaryDirectory
from pathlib import Path


from fastapi import UploadFile, File, HTTPException
from pathlib import Path
from tempfile import TemporaryDirectory

from app.modules.m1_ocr.extractor import extract_pdf_text
from app.modules.m2_classification.pipeline import analyze_document_clauses




from pydantic import BaseModel
from typing import Optional

from app.modules.m2_classification.pipeline import (
    analyze_document_clauses
)

class M2AnalyzeRequest(BaseModel):
    text: str
    domain: Optional[str] = None


app = FastAPI(
    title="Legal Intelligence AI Service",
    description="AI APIs for legal document analysis",
    version="1.0.0"
)
app.include_router(legal_search_router)
# Configure this with your frontend/backend origin in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


ALLOWED_TYPES = {
    "employment",
    "job_offer",
    "divorce_family",
    "property",
    "rental"
}


class TextRequest(BaseModel):
    text: str
    document_type: str = "employment"


class TranslateRequest(BaseModel):
    text: str
    target_language: str = "marathi"


class AskRequest(BaseModel):
    text: str
    question: str


def validate_document_type(document_type):
    if document_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Invalid document type"
        )


def validate_pdf(filename):
    if not filename or not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )


async def save_uploaded_pdf(file: UploadFile):

    validate_pdf(file.filename)

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    # Temporary file is removed after processing.
    temp = tempfile.NamedTemporaryFile(
        suffix=".pdf",
        delete=False
    )

    try:
        temp.write(content)
        temp.close()
        return temp.name

    except Exception:
        temp.close()
        Path(temp.name).unlink(missing_ok=True)
        raise


def extract_text_from_path(path):

    result = extract_pdf_text(path)

    text = result.get("full_text", "")

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No text could be extracted"
        )

    return text


@app.get("/")
def home():
    return {
        "service": "Legal Intelligence AI Service",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "ai-service"
    }


@app.post("/api/ai/extract")
async def extract_api(file: UploadFile = File(...)):

    path = await save_uploaded_pdf(file)

    try:
        result = extract_pdf_text(path)
        return result

    finally:
        Path(path).unlink(missing_ok=True)


@app.post("/api/ai/classify")
async def classify_api(
    text: str = Form(...),
    document_type: str = Form("employment")
):

    validate_document_type(document_type)

    if not text.strip():
        raise HTTPException(400, "Text is required")

    return {
        "document_type": document_type,
        "result": classify_document(text)
    }


@app.post("/api/ai/missing-clauses")
async def missing_clauses_api(request: TextRequest):

    validate_document_type(request.document_type)

    if not request.text.strip():
        raise HTTPException(400, "Text is required")

    return detect_missing_clauses(
        request.text,
        request.document_type
    )


@app.post("/api/ai/risk")
async def risk_api(request: TextRequest):

    validate_document_type(request.document_type)

    if not request.text.strip():
        raise HTTPException(400, "Text is required")

    return calculate_risk(
        request.text,
        request.document_type
    )


@app.post("/api/ai/fairness")
async def fairness_api(request: TextRequest):

    validate_document_type(request.document_type)

    if not request.text.strip():
        raise HTTPException(400, "Text is required")

    return analyze_fairness(
        request.text,
        request.document_type
    )


@app.post("/api/ai/ask")
async def ask_api(request: AskRequest):

    if not request.text.strip() or not request.question.strip():
        raise HTTPException(
            400,
            "Document text and question are required"
        )

    try:
        qa = LegalQA()
        qa.index_document(request.text)

        return qa.ask_question(request.question)

    except Exception as error:
        raise HTTPException(
            500,
            detail=f"Legal Q&A failed: {str(error)}"
        )


@app.post("/api/ai/compare")
async def compare_api(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):

    path1 = await save_uploaded_pdf(file1)
    path2 = await save_uploaded_pdf(file2)

    try:
        text1 = extract_text_from_path(path1)
        text2 = extract_text_from_path(path2)

        comparator = AgreementComparator()

        return comparator.compare_documents(
            text1,
            text2
        )

    finally:
        Path(path1).unlink(missing_ok=True)
        Path(path2).unlink(missing_ok=True)


@app.post("/api/m2/analyze")
def analyze_m2(request: M2AnalyzeRequest):

    result = analyze_document_clauses(
        text=request.text,
        domain=request.domain
    )

    return {
        "status": "success",
        "module": "M2 - Clause Classification",
        "result": result
    }


@app.post("/api/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    """Run OCR and clause classification on an uploaded PDF."""

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    with TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / "uploaded_document.pdf"

        # Save uploaded PDF in chunks
        with pdf_path.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                output.write(chunk)

        # M1: Extract document text
        ocr_result = extract_pdf_text(pdf_path)
        document_text = ocr_result["full_text"]

        if not document_text.strip():
            raise HTTPException(
                status_code=422,
                detail="No readable text found in the PDF."
            )

        # M2: Detect domain and classify clauses
        classification_result = analyze_document_clauses(
            document_text
        )

        if classification_result.get("error"):
            raise HTTPException(
                status_code=422,
                detail=classification_result["error"]
            )

        return {
            "status": "success",
            "filename": file.filename,
            "document_type": classification_result["domain"],
            "ocr": {
                "page_count": ocr_result["page_count"],
                "text_length": len(document_text)
            },
            "classification": classification_result
        }



@app.post("/api/analyze-complete")
async def analyze_complete(
    file: UploadFile = File(...),
    target_language: str = "Hindi",
    document_type: str = None
):

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    with TemporaryDirectory() as temp_dir:

        pdf_path = Path(temp_dir) / "uploaded_document.pdf"

        with pdf_path.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                output.write(chunk)

        try:
            result = run_legal_ai_pipeline(
                pdf_path=pdf_path,
                target_language=target_language,
                document_type=document_type
            )

            return result

        except ValueError as error:
            raise HTTPException(
                status_code=422,
                detail=str(error)
            )
           

        except Exception as error:
            import traceback
            traceback.print_exc()

            raise HTTPException(
                status_code=500,
                detail=f"{type(error).__name__}: {str(error)}"
            )

from app.modules.m8_rag.legal_knowledge_base import LegalKnowledgeBase


@app.post("/api/legal-knowledge/add")
async def add_legal_knowledge(
    file: UploadFile = File(...),
    title: str = Form(...),
    source_url: str = Form(...),
    domain: str = Form(...),
    jurisdiction: str = Form("India"),
    effective_date: Optional[str] = Form(None),
    version: str = Form("1")
):

    validate_pdf(file.filename)

    path = await save_uploaded_pdf(file)

    try:
        kb = LegalKnowledgeBase()

        return kb.add_legal_document(
            pdf_path=path,
            title=title,
            source_url=source_url,
            domain=domain,
            jurisdiction=jurisdiction,
            effective_date=effective_date,
            version=version
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error)
        )

    finally:
        Path(path).unlink(missing_ok=True)


class LegalSearchRequest(BaseModel):
    question: str
    top_k: int = 5
    domain: Optional[str] = None
    jurisdiction: Optional[str] = None


@app.post("/api/legal-knowledge/search")
def search_legal_knowledge(request: LegalSearchRequest):

    kb = LegalKnowledgeBase()

    return kb.search(
        question=request.question,
        top_k=request.top_k,
        domain=request.domain,
        jurisdiction=request.jurisdiction
    )

# NOTE:
# Summarization and translation are intentionally not wired here yet.
# Their exact public function names and arguments need to match the
# implementations in your m3_summarization and m4_translation files.