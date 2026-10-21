# Legal Intelligence AI — End-to-End Autonomous Legal Analysis Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-cyan.svg)](https://react.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-4.0-38bdf8.svg)](https://tailwindcss.com/)
[![FAISS](https://img.shields.io/badge/FAISS-CPU-orange.svg)](https://github.com/facebookresearch/faiss)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An end-to-end, research-grade Legal Intelligence AI system designed for Indian legal documents, agreements, and statutes. Integrates document OCR, multi-domain clause classification, abstractive summarization, multilingual translation (English, Hindi, Marathi), checklist-based missing clause detection, risk scoring, fairness analysis, citation-grounded FAISS RAG, document version comparison, downloadable reports, and a responsive React frontend based on the Framer design system.

---

## Architecture Overview

```
                                      ┌──────────────────────────────────────────────┐
                                      │   React 19 Frontend (Framer Design System)   │
                                      │  Upload · Analysis · Dashboard · QA · Compare│
                                      └──────────────────────┬───────────────────────┘
                                                             │ REST / JSON (JWT / Firebase)
                                      ┌──────────────────────▼───────────────────────┐
                                      │            FastAPI Unified Server            │
                                      │              (Port 8000)                     │
                                      └───────┬───────────────────────────────┬──────┘
                                              │                               │
                       ┌──────────────────────▼──────┐         ┌──────────────▼──────────────┐
                       │    Core AI Pipeline (M1-M9) │         │ Persistence & Auth Layer    │
                       ├─────────────────────────────┤         ├─────────────────────────────┤
                       │ M1: PyMuPDF / Tesseract OCR │         │ • Firebase Auth & Firestore │
                       │ M2: Hybrid Clause Classifier│         │ • Local SQLite & JWT backup │
                       │ M3: BART Abstractive Sum.   │         │ • Encrypted Document Storage│
                       │ M4: NLLB Multilingual (HI/MR)         └─────────────────────────────┘
                       │ M5: Missing Clause Detection│
                       │ M6: Penalty-Rule Risk Engine│
                       │ M7: Asymmetry Fairness Model│
                       │ M8: FAISS Legal RAG (3,092v)│
                       │ M9: Pairwise Clause Diffing │
                       └─────────────────────────────┘
```

---

## Module Breakdown (M1–M9)

- **M1 — OCR & Text Extraction**: High-fidelity digital text extraction via PyMuPDF with Tesseract OCR fallback for scanned pages.
- **M2 — Legal Clause Classification**: 4-domain classification (Employment, Rental, Property, Divorce) utilizing a hybrid keyword-guided semantic approach (`all-MiniLM-L6-v2`) delivering **87.50% accuracy at 15.76 ms/clause (23.6× faster than pure dense search)**.
- **M3 — Summarization**: Facebook BART (`facebook/bart-large-cnn`) with non-truncating uniform document chunk sampling.
- **M4 — Multilingual Translation**: Low-resource Indian language translation (`facebook/nllb-200-distilled-600M`) supporting English, Hindi (`hin_Deva`), and Marathi (`mar_Deva`).
- **M5 — Missing Clause Detection**: Mandatory statutory clause checklists across 5 agreement categories to ensure critical protections are present.
- **M6 — Risk Scoring Engine**: Weighted penalty rule engine evaluating omitted clauses, non-standard terms, and compliance risks.
- **M7 — Fairness Scoring**: Detection of contractual asymmetries (unilateral termination, unlimited liability, broad indemnity, punitive damages).
- **M8 — Citation-Grounded Legal RAG**: Dense vector index over 3,092 legal passages across 16 core Indian statutes and official government enactments with **28.42 ms retrieval latency**.
- **M9 — Document Comparison**: Heuristic clause alignment and numerical delta analysis identifying wording modifications, omitted clauses, and new insertions.

---

## Quick Start

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- (Optional) Git, Tesseract OCR

### 2. Backend Setup
```powershell
# Clone repository
git clone <repository-url>
cd legal-intelligence

# Activate existing virtual environment (or create one)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
API Documentation will be live at: `http://localhost:8000/docs`

### 3. Frontend Setup
```powershell
cd frontend

# Install packages
npm install

# Build static assets (served automatically by FastAPI at http://localhost:8000/)
npm run build

# OR run Vite hot-reload development server
npm run dev
```
Development server will be live at: `http://localhost:5173`

---

## Web Application Screens

1. **Upload Document (`/upload`)**: Drag-and-drop PDF upload with progress feedback and automatic file validation.
2. **AI Analysis Hub (`/analysis/:documentId`)**: Multi-section view presenting extracted clauses, executive summary, risk level, and fairness scores.
3. **Risk & Fairness Dashboard (`/dashboard`)**: Metric cards, interactive risk meters, bias indicators, and recent audit history.
4. **Legal AI Chat (`/qa`)**: Citation-grounded document Q&A backed by FAISS vector similarity and statutory evidence.
5. **Document Comparison (`/compare`)**: Side-by-side agreement diffing highlighting modified text, altered numbers/amounts, and new terms.
6. **Reports (`/reports`)**: Downloadable text and localized summaries in English, Hindi, and Marathi.

---

## Firebase Integration & Configuration

The application includes production-grade Firebase integration with an automatic local fallback (SQLite + JWT):
- **Authentication**: Firebase ID Token verification via `firebase-admin` with local signed JWT fallback.
- **Firestore**: User profiles, document metadata, and analysis history synced to Firestore.
- **Cloud Storage**: Uploaded agreement PDFs stored securely in Firebase Storage buckets.

To activate live Firebase cloud services, add your credentials to `.env`:
```env
FIREBASE_CREDENTIALS_PATH=./firebase-service-account.json
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
```
In `frontend/.env`:
```env
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
```

---

## IEEE Research Benchmark & Reproduction

To reproduce the empirical research evaluation results:

```powershell
# Run full module import test
python -m evaluation.run_all_evaluations

# Run M1 OCR evaluation
python -m evaluation.evaluate_m1

# Run M2 Clause Classification model comparison (Keyword vs Semantic vs Hybrid)
python -m evaluation.evaluate_m2_comparison

# Run M3 BART Summarization ROUGE scoring
python -m evaluation.evaluate_m3

# Run M4 NLLB Multilingual Translation BLEU & chrF++ benchmark
python -m evaluation.evaluate_m4

# Run M5 Missing Clause detection test
python -m evaluation.evaluate_m5

# Run M7 Fairness Indicator precision & recall
python -m evaluation.evaluate_m7

# Run M8 FAISS RAG Retrieval latency and hit-rate benchmark
python ieee_rag_benchmark.py

# Run M9 Agreement Comparison evaluation
python -m evaluation.evaluate_m9

# Generate publication figures
python -m evaluation.plot_m1_graphs
python -m evaluation.plot_m2_comparison
```

Consolidated research evidence and results are archived in:
- `IEEE_EVIDENCE/IEEE_RESULTS.md`
- `IEEE_EVIDENCE/results.csv`
- `IEEE_EVIDENCE/metrics.json`
- `IEEE_EVIDENCE/figures/`
- `IEEE_EVIDENCE/tables/`

---

## Security & Data Privacy

1. **No Cloud Leakage of Sensitive Contracts**: The entire pipeline (PyMuPDF, BART, NLLB, FAISS) runs locally on CPU/GPU without transmitting documents to third-party paid AI APIs (OpenAI, Gemini, Anthropic).
2. **Access Control**: Users are partitioned by authentication tokens; document queries and history require valid ownership claims.
3. **Sensitive File Exclusions**: Private documents, local database caches, and service keys are protected via `.gitignore`.

---

## License

This project is licensed under the MIT License.
