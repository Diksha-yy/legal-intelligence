# DEPLOYMENT GUIDE — LEGAL INTELLIGENCE AI

This guide outlines deployment options for Legal Intelligence AI across cloud platforms and local infrastructure.

---

## Architecture Requirements
- **Frontend**: Static SPA (HTML, CSS, JS bundle, assets). Memory footprint: < 50MB. Can be hosted anywhere on free static tiers (Vercel, Cloudflare Pages, Firebase Hosting, Netlify).
- **Backend**: Python 3.11 with PyTorch (`torch`), PyMuPDF, Transformers (`facebook/bart-large-cnn`), NLLB (`nllb-200-distilled-600M`), and FAISS. Minimum RAM recommendation: **4 GB RAM** (for CPU inference) or any machine with an NVIDIA GPU (2 GB VRAM).
- **Database / Storage**: Firebase Free Tier (Spark Plan) provides 1 GB Firestore storage and 5 GB Cloud Storage at zero cost.

---

## Option 1: Unified Single-Container Deployment (Recommended)

FastAPI serves both the REST API endpoints and the built React frontend from `/frontend/dist`.

### Docker Run
```bash
docker build -t legal-intelligence:latest .
docker run -d -p 8000:8000 --name legal-ai legal-intelligence:latest
```

### Docker Compose
```bash
docker compose up -d --build
```
Access the application at `http://localhost:8000`.

---

## Option 2: Split Cloud Deployment (Free Tiers)

### 1. Frontend on Vercel or Cloudflare Pages (Free)
1. In the `frontend/` folder, run `npm run build`.
2. Connect your GitHub repository to Vercel or Cloudflare Pages.
3. Configure build settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Set environment variable:
   - `VITE_API_BASE_URL`: `https://your-backend-domain.com`

### 2. Backend on Render / Railway / Fly.io / Hugging Face Spaces
- **Hugging Face Spaces (Free Docker / CPU)**:
  - Create a new Space with the **Docker** SDK.
  - Push the repository to the Space.
  - Set `PORT=7860` in Space settings or Dockerfile.
  - Hugging Face provides **16 GB RAM free**, which easily accommodates BART and NLLB translation models without memory exhaustion.
- **Render / Railway / Fly.io**:
  - Deploy using the provided `Dockerfile`.
  - Ensure the instance has at least 2 GB RAM (4 GB recommended for BART summarization).

### 3. Firebase Free Spark Plan Configuration
1. Go to [Firebase Console](https://console.firebase.google.com/) and create a new project.
2. Under **Project Settings > Service accounts**, generate a new private key and save as `firebase-service-account.json`.
3. Enable **Authentication** (Email/Password and Google sign-in).
4. Enable **Cloud Firestore** in production mode.
5. Enable **Cloud Storage** for legal PDF uploads.
6. Provide the environment variables in `.env`:
   ```env
   FIREBASE_CREDENTIALS_PATH=/path/to/firebase-service-account.json
   FIREBASE_STORAGE_BUCKET=your-project.appspot.com
   ```

---

## Option 3: Local Production / Demonstration Run

To run the application locally on Windows without Docker:

```powershell
# 1. Activate environment
cd C:\Users\DIKSHA\legal-intelligence
.\.venv\Scripts\Activate.ps1

# 2. Build the React frontend
cd frontend
npm run build
cd ..

# 3. Start FastAPI with production workers
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Open your browser to:
- **Application UI**: `http://localhost:8000/`
- **Swagger Documentation**: `http://localhost:8000/docs`
