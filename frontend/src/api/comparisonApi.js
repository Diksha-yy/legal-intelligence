import client from "./client";

/**
 * POST /api/agreement-comparison
 * Compare two documents by ID.
 * @param {{ versionADocumentId: number, versionBDocumentId: number }} request
 * @returns {Promise<AgreementComparisonResponse>}
 */
export function compareAgreements(request) {
  return client.post("/api/agreement-comparison", request).then((r) => r.data);
}

/**
 * GET /api/agreement-comparison/{comparisonId}
 */
export function getComparisonById(comparisonId) {
  return client.get(`/api/agreement-comparison/${comparisonId}`).then((r) => r.data);
}

/**
 * GET /api/agreement-comparison/history/{documentId}
 * @returns {Promise<AgreementComparisonResponse[]>}
 */
export function getComparisonHistory(documentId) {
  return client
    .get(`/api/agreement-comparison/history/${documentId}`)
    .then((r) => r.data);
}

/**
 * DELETE /api/agreement-comparison/{comparisonId}
 */
export function deleteComparison(comparisonId) {
  return client
    .delete(`/api/agreement-comparison/${comparisonId}`)
    .then((r) => r.data);
}
