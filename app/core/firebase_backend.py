"""
Firebase Integration & Storage Manager for Legal Intelligence AI.

Provides:
- Firebase Admin initialization with service-account or default credentials.
- Firebase ID Token verification (with local JWT fallback for offline/local development).
- Firestore document metadata & analysis history persistence (with local SQLite fallback).
- Firebase Cloud Storage for uploaded PDFs and generated reports (with local storage fallback).
- User-level access control & data privacy safeguards.
"""
from __future__ import annotations

import os
import json
import sqlite3
import jwt
import time
from pathlib import Path
from typing import Optional, Dict, Any, List

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
DB_PATH = DATA_DIR / "legal_intelligence.db"

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Secret key for local JWT fallback
LOCAL_JWT_SECRET = os.getenv("JWT_SECRET", "legal-ai-secret-key-production-change-me")
JWT_ALGORITHM = "HS256"

# Firebase Admin state
_firebase_initialized = False
_firestore_db = None
_storage_bucket = None

def init_firebase() -> bool:
    """Initialize Firebase Admin SDK if credentials are present."""
    global _firebase_initialized, _firestore_db, _storage_bucket
    if _firebase_initialized:
        return True

    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    cred_json = os.getenv("FIREBASE_CONFIG_JSON")

    # Check for service account json in config or root
    default_cred_files = [
        ROOT_DIR / "firebase-service-account.json",
        ROOT_DIR / "serviceAccountKey.json",
        ROOT_DIR / "app" / "core" / "firebase-service-account.json"
    ]

    for p in default_cred_files:
        if p.is_file():
            cred_path = str(p)
            break

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore, storage

        if cred_path and Path(cred_path).is_file():
            cred = credentials.Certificate(cred_path)
            bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")
            firebase_admin.initialize_app(cred, {"storageBucket": bucket_name} if bucket_name else None)
            _firebase_initialized = True
        elif cred_json:
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
            bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")
            firebase_admin.initialize_app(cred, {"storageBucket": bucket_name} if bucket_name else None)
            _firebase_initialized = True
        else:
            # Check default app
            try:
                firebase_admin.get_app()
                _firebase_initialized = True
            except ValueError:
                # No default app and no credentials provided yet
                _firebase_initialized = False
                return False

        _firestore_db = firestore.client()
        bucket_name = os.getenv("FIREBASE_STORAGE_BUCKET")
        if bucket_name:
            _storage_bucket = storage.bucket(bucket_name)
        print("[Firebase] Firebase Admin SDK successfully initialized.")
        return True
    except Exception as exc:
        print(f"[Firebase] Firebase initialization skipped/failed: {exc}. Using local storage fallback.")
        _firebase_initialized = False
        return False


def get_sqlite_conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_local_database():
    """Create local SQLite tables for documents, analyses, Q&A, comparisons, and users."""
    conn = get_sqlite_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password_hash TEXT,
        role TEXT DEFAULT 'CLIENT',
        created_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        title TEXT,
        file_name TEXT,
        file_path TEXT,
        file_size INTEGER,
        document_type TEXT,
        extracted_text TEXT,
        status TEXT DEFAULT 'UPLOADED',
        uploaded_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clauses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        clause_name TEXT,
        clause_text TEXT,
        confidence REAL,
        risk_level TEXT,
        created_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER UNIQUE,
        summary TEXT,
        key_points TEXT,
        chunks_processed INTEGER,
        model_name TEXT,
        created_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS risk_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER UNIQUE,
        risk_score REAL,
        risk_level TEXT,
        explanation TEXT,
        findings TEXT,
        recommendations TEXT,
        created_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fairness_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER UNIQUE,
        fairness_score REAL,
        fairness_level TEXT,
        bias_detected INTEGER,
        explanation TEXT,
        clauses_analyzed TEXT,
        created_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS qa_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        question TEXT,
        answer TEXT,
        confidence_score REAL,
        llm_model TEXT,
        retrieved_clauses TEXT,
        created_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS translations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        source_language TEXT,
        target_language TEXT,
        translated_text TEXT,
        created_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS comparisons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        doc_a_id INTEGER,
        doc_b_id INTEGER,
        comparison_status TEXT,
        comparison_summary TEXT,
        total_clauses INTEGER,
        matched_clauses INTEGER,
        modified_clauses INTEGER,
        added_clauses INTEGER,
        removed_clauses INTEGER,
        clause_differences TEXT,
        created_at TEXT
    )
    """)
    conn.commit()
    conn.close()


init_local_database()
init_firebase()


def verify_auth_token(token: str) -> Dict[str, Any]:
    """Verify either a Firebase ID token or a local JWT token."""
    if not token:
        raise ValueError("Missing authentication token")

    # If Firebase initialized, try verifying as Firebase ID token
    if _firebase_initialized:
        try:
            import firebase_admin.auth
            decoded = firebase_admin.auth.verify_id_token(token)
            return {
                "uid": decoded.get("uid"),
                "email": decoded.get("email", ""),
                "name": decoded.get("name", ""),
                "role": decoded.get("role", "CLIENT"),
                "source": "firebase"
            }
        except Exception:
            pass  # Fall through to local JWT verification

    # Verify local JWT
    try:
        payload = jwt.decode(token, LOCAL_JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception as exc:
        raise ValueError(f"Invalid authentication token: {exc}")


def create_local_jwt(user: Dict[str, Any]) -> str:
    """Create local signed JWT token."""
    payload = {
        "id": user.get("id"),
        "email": user.get("email"),
        "name": user.get("name", ""),
        "role": user.get("role", "CLIENT"),
        "exp": int(time.time()) + 86400 * 7,  # 7 days
        "source": "local"
    }
    return jwt.encode(payload, LOCAL_JWT_SECRET, algorithm=JWT_ALGORITHM)


def save_document_file(file_bytes: bytes, filename: str) -> str:
    """Save document locally or upload to Firebase Storage if configured."""
    local_path = UPLOADS_DIR / f"{int(time.time())}_{filename}"
    local_path.write_bytes(file_bytes)

    if _firebase_initialized and _storage_bucket:
        try:
            blob = _storage_bucket.blob(f"documents/{local_path.name}")
            blob.upload_from_filename(str(local_path))
        except Exception as exc:
            print(f"[Firebase] Storage upload error: {exc}")

    return str(local_path)


def save_firestore_record(collection: str, doc_id: str, data: Dict[str, Any]):
    """Sync record to Firestore if active."""
    if _firebase_initialized and _firestore_db:
        try:
            _firestore_db.collection(collection).document(str(doc_id)).set(data, merge=True)
        except Exception as exc:
            print(f"[Firebase] Firestore set error: {exc}")
