import client from "./client";

/**
 * POST /api/translation/generate/{documentId}?sourceLanguage=en&targetLanguage=hi
 * @param {number} documentId
 * @param {string} sourceLanguage  ISO 639-1 code (en | hi | mr)
 * @param {string} targetLanguage  ISO 639-1 code (en | hi | mr)
 * @returns {Promise<DocumentTranslationResponse>}
 */
export function generateTranslation(documentId, sourceLanguage, targetLanguage) {
  return client
    .post(`/api/translation/generate/${documentId}`, null, {
      params: { sourceLanguage, targetLanguage },
    })
    .then((r) => r.data);
}

/**
 * GET /api/translation/{documentId}
 * Retrieve the most recent stored translation.
 * @returns {Promise<DocumentTranslationResponse>}
 */
export function getTranslation(documentId) {
  return client.get(`/api/translation/${documentId}`).then((r) => r.data);
}
