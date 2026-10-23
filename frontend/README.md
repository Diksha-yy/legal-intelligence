# Legal Assistant Frontend

This ZIP contains the frontend source only. Dependencies and build output are intentionally excluded.

## Included updates
- Merged Claude's partial `frontend-updated.zip` changes into the original frontend source.
- Added individual routes for analysis sections: `/analysis/:documentId/:section`.
- Risk score colors: red below 50, yellow from 50 through 74, green from 75 onward.
- Added complete English, Hindi and Marathi UI translations for the homepage, authentication, dashboard, document upload/list, OCR processing, analysis, Q&A, comparison, reports, profile/settings, shared navigation and footer.
- Added a responsive mobile navigation menu with active-route states, account sign-out and working links to the document library and upload flow.
- Removed fabricated homepage statistics and sample analysis results, along with inactive navigation controls.
- Updated dashboard, processing and analysis pages to use the existing backend API services instead of hardcoded document/analysis results.
- Made `/register` open registration directly, restored protected-route destinations after login, and removed the unsupported password-reset link.
- Enforced the upload page's supported file extensions and 20MB size limit; OCR polling now waits for the start request and retains its timeout across status updates.
- Surfaced document-list and analysis-fetch failures instead of silently presenting empty results.

## Run locally
1. Install Node.js (use a version compatible with the Vite version in `package.json`).
2. Run `npm install`.
3. Copy `.env.example` to `.env` and set `VITE_API_BASE_URL` to your Spring Boot backend URL.
4. Start the Spring Boot backend and confirm that its API is reachable at the configured URL.
5. Run `npm run dev`, then open the Vite URL in the browser. Restart Vite whenever `.env` changes.

Protected module navigation stays in the same browser tab so the tab-scoped login session is preserved. Directly opening a protected route without a valid session sends the user to login and returns them to that route after a successful login.

## Backend and AI integration contract

This repository contains the frontend only. The browser calls the backend at `VITE_API_BASE_URL`; keep database credentials, AI provider keys, and calls to private AI services on the server. The backend should orchestrate OCR and AI work and expose the HTTP endpoints below. Authenticated requests carry `Authorization: Bearer <token>`. The document upload request is `multipart/form-data`; the browser sets its boundary automatically.

| Workflow | Endpoint | Request | Frontend-used response fields |
|---|---|---|---|
| Register | `POST /api/users/register` | `{ name, email, password, role }` | Successful 2xx response; frontend then logs in |
| Login | `POST /api/auth/login` | `{ email, password }` | `{ token }` |
| List documents | `GET /api/documents` | — | Array of `{ id, title, fileName, status, uploadedAt, uploadedBy }` |
| Upload document | `POST /api/documents/upload` | multipart fields `file`, `title` | `{ id, title, fileName, status }` |
| Get document | `GET /api/documents/{id}` | — | Document fields above |
| Start OCR | `POST /api/ocr/start/{id}` | — | Accepted job response |
| Poll OCR | `GET /api/ocr/{id}` | — | `{ status, extractedText }`; terminal status `COMPLETED` or `FAILED` |
| Summary | `POST /api/summary/generate/{id}`, `GET /api/summary/{id}` | — | `{ summary, summaryModel }` |
| Clauses | `POST /api/clauses/classify/{id}`, `GET /api/clauses/document/{id}` | — | Array of `{ id, clauseName, clauseText, confidence }` |
| Risk | `POST /api/risk-score/analyze/{id}`, `GET /api/risk-score/{id}` | — | `{ riskScore, riskLevel, explanation, riskFactors }` |
| Fairness | `POST /api/fairness/analyze/{id}`, `GET /api/fairness/{id}` | — | `{ fairnessScore, explanation }` and available party rights/obligations/penalties |
| Missing clauses | `GET /api/missing-clauses/check?documentId={id}&documentTypeId={type}` | Query parameters | Missing/mandatory clause counts and details |
| Legal Q&A | `POST /api/qa/{id}`, `GET /api/qa/{id}` | JSON string question | `{ id, question, answer, createdAt, confidenceScore, retrievedClauses }` / array |
| Agreement comparison | `POST /api/agreement-comparison` | `{ versionADocumentId, versionBDocumentId }` | Comparison status, summary, counts and clause differences |
| Translation | `POST /api/translation/generate/{id}?sourceLanguage={en\|hi\|mr}&targetLanguage={en\|hi\|mr}`, `GET /api/translation/{id}` | — | `{ sourceLanguage, targetLanguage, translatedText, translationModel }` |

Additional endpoints used by the interface:

| Feature | Endpoint |
|---|---|
| Delete a document | `DELETE /api/documents/{id}` |
| Read one clause | `GET /api/clauses/{clauseId}` |
| Read/delete a Q&A record | `GET /api/qa/record/{queryId}`, `DELETE /api/qa/record/{queryId}` |
| Clear a document's Q&A history | `DELETE /api/qa/{documentId}/history` |
| Read comparison/history/delete comparison | `GET /api/agreement-comparison/{comparisonId}`, `GET /api/agreement-comparison/history/{documentId}`, `DELETE /api/agreement-comparison/{comparisonId}` |

Document IDs are expected to be numeric because comparison, chat, and report requests convert selected IDs to numbers. The login response must include a non-empty `token` field; registration is followed by a login request.

Return JSON errors using `{ "message": "Human-readable explanation" }` where possible. Use 401 for expired/invalid authentication, 403 for authorization failures, 404 when a requested resource/result does not exist yet, 422 when a workflow prerequisite is missing, and 5xx for backend/AI service failures. AI endpoints may return 503 when a provider is unavailable. The frontend treats missing analysis results (404) as not-yet-generated states.

For local development, configure backend CORS to allow the exact Vite origin used in the browser (commonly `http://localhost:5173` or `http://127.0.0.1:5173`), the `Authorization` and `Content-Type` request headers, and the methods used by the API (`GET`, `POST`, `DELETE`, `OPTIONS`). If the backend uses cookie authentication instead of the documented bearer-token contract, configure credentials on both sides rather than exposing tokens in URLs.

The document processing page can be refreshed safely: its document ID and filename are retained in the URL query string. The OCR poller accepts `COMPLETED`/`FAILED` as canonical status values and also normalizes common aliases (`DONE`, `SUCCESS`, `RUNNING`, `IN_PROGRESS`, `QUEUED`, `ERROR`, `CANCELLED`).

## Language support
- The interface language selector supports English, Hindi and Marathi and persists the choice in local storage.
- Report translation is a separate backend AI feature; the backend must support ISO-639-1 codes `en`, `hi` and `mr` for the corresponding options to work.
- AI-generated summaries, answers and translated document text are shown as returned by the backend, not machine-translated by the interface.

## Validation
- `npm run build` checks the production bundle.
- `npm run lint` checks the project. Any remaining lint issue should be fixed at its source before integration.
- Backend integration still requires a running backend and AI services configured for the endpoint contract above.
- A frontend build does not validate Spring controller mappings, security rules, CORS, database connectivity, or AI services; test those against the running backend.
