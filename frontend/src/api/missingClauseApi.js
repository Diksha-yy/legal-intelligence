import client from "./client";

/**
 * GET /api/missing-clauses/check?documentId=X&documentTypeId=Y
 * @param {number} documentId
 * @param {number} documentTypeId
 * @returns {Promise<MissingClauseResponse>}
 */
export function detectMissingClauses(documentId, documentTypeId) {
  return client
    .get("/api/missing-clauses/check", {
      params: { documentId, documentTypeId },
    })
    .then((r) => r.data);
}
