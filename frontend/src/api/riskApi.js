import client from "./client";

/**
 * POST /api/risk-score/analyze/{documentId}
 * Trigger risk analysis.
 * @returns {Promise<RiskScoreResponse>}
 */
export function analyzeRisk(documentId) {
  return client.post(`/api/risk-score/analyze/${documentId}`).then((r) => r.data);
}

/**
 * GET /api/risk-score/{documentId}
 * Retrieve the stored risk score.
 * @returns {Promise<RiskScoreResponse>}
 */
export function getRiskScore(documentId) {
  return client.get(`/api/risk-score/${documentId}`).then((r) => r.data);
}
