import client from "./client";

/**
 * POST /api/clauses/classify/{documentId}
 * Trigger Python clause classification. Returns ClauseResponse[].
 */
export function classifyClauses(documentId) {
  return client.post(`/api/clauses/classify/${documentId}`).then((r) => r.data);
}

/**
 * GET /api/clauses/document/{documentId}
 * Retrieve all classified clauses for a document.
 * @returns {Promise<ClauseResponse[]>}
 */
export function getClausesByDocument(documentId) {
  return client.get(`/api/clauses/document/${documentId}`).then((r) => r.data);
}

/**
 * GET /api/clauses/{clauseId}
 */
export function getClauseById(clauseId) {
  return client.get(`/api/clauses/${clauseId}`).then((r) => r.data);
}
