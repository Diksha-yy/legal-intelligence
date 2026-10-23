import client from "./client";

/**
 * POST /api/qa/{documentId}
 * Ask a legal question about a document.
 * The request body is a plain string (the question).
 * Backend retrieves document context from MySQL.
 * @param {number} documentId
 * @param {string} question
 * @returns {Promise<DocumentLegalQueryResponse>}
 */
export function askQuestion(documentId, question) {
  return client
    .post(`/api/qa/${documentId}`, question, {
      headers: { "Content-Type": "application/json" },
    })
    .then((r) => r.data);
}

/**
 * GET /api/qa/{documentId}
 * Retrieve Q&A history for the document (newest first).
 * @returns {Promise<DocumentLegalQueryResponse[]>}
 */
export function getQaHistory(documentId) {
  return client.get(`/api/qa/${documentId}`).then((r) => r.data);
}

/**
 * GET /api/qa/record/{queryId}
 */
export function getQaRecord(queryId) {
  return client.get(`/api/qa/record/${queryId}`).then((r) => r.data);
}

/**
 * DELETE /api/qa/record/{queryId}
 */
export function deleteQaRecord(queryId) {
  return client.delete(`/api/qa/record/${queryId}`).then((r) => r.data);
}

/**
 * DELETE /api/qa/{documentId}/history
 */
export function clearQaHistory(documentId) {
  return client.delete(`/api/qa/${documentId}/history`).then((r) => r.data);
}
