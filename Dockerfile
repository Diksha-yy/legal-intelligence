# ===============================================================
# Multi-stage Dockerfile for Legal Intelligence AI
# Stage 1: Build React Framer-styled frontend
# Stage 2: Python FastAPI Backend with PyTorch, FAISS & Preloaded Models
# ===============================================================

FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# ===============================================================
# Stage 2: Runtime Backend
# ===============================================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PORT=8000

# Install system dependencies for OCR & PyMuPDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-hin \
    tesseract-ocr-mar \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy codebase
COPY app/ ./app/
COPY data/ ./data/
COPY models/ ./models/
COPY legal_law_collector/ ./legal_law_collector/
COPY IEEE_EVIDENCE/ ./IEEE_EVIDENCE/
COPY evaluation/ ./evaluation/

# Copy built frontend assets from stage 1 into frontend/dist
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
