import client from "./client";

/**
 * POST /api/summary/generate/{documentId}
 * Generate a summary for the document.
 * @returns {Promise<DocumentSummaryResponse>}
 */
export function generateSummary(documentId) {
  return client.post(`/api/summary/generate/${documentId}`).then((r) => r.data);
}

/**
 * GET /api/summary/{documentId}
 * Retrieve the existing summary.
 * @returns {Promise<DocumentSummaryResponse>}
 */
export function getSummary(documentId) {
  return client.get(`/api/summary/${documentId}`).then((r) => r.data);
}
