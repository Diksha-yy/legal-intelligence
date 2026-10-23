import client from "./client";

/**
 * POST /api/ocr/start/{documentId}
 * Starts OCR for the document. Returns 202 Accepted + OcrJobResponse.
 */
export function startOcr(documentId) {
  return client.post(`/api/ocr/start/${documentId}`).then((r) => r.data);
}

/**
 * GET /api/ocr/{documentId}
 * Poll OCR job status.
 * @returns {Promise<OcrJobResponse>}  { id, documentId, status, extractedText, ... }
 */
export function getOcrStatus(documentId) {
  return client.get(`/api/ocr/${documentId}`).then((r) => r.data);
}
