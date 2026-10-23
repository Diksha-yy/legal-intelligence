import client from "./client";

/**
 * POST /api/fairness/analyze/{documentId}
 * Trigger fairness analysis (requires OCR + clause classification).
 * @returns {Promise<FairnessScoreResponse>}
 */
export function analyzeFairness(documentId) {
  return client.post(`/api/fairness/analyze/${documentId}`).then((r) => r.data);
}

/**
 * GET /api/fairness/{documentId}
 * Retrieve the stored fairness result.
 * @returns {Promise<FairnessScoreResponse>}
 */
export function getFairnessScore(documentId) {
  return client.get(`/api/fairness/${documentId}`).then((r) => r.data);
}
