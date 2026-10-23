import client, { API_BASE_URL } from "./client";

/**
 * POST /api/documents/upload  (multipart/form-data)
 * @param {File} file
 * @param {string} title
 * @returns {Promise<DocumentResponse>}
 */
export function uploadDocument(file, title) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("title", title);
  return client
    .post("/api/documents/upload", formData, {
      // Let the browser set the multipart boundary.
    })
    .then((r) => r.data);
}

/**
 * GET /api/documents
 * @returns {Promise<DocumentResponse[]>}
 */
export function getAllDocuments() {
  return client.get("/api/documents").then((r) => {
    if (!Array.isArray(r.data)) {
      throw new Error("The server returned an invalid documents response.");
    }
    return r.data;
  });
}

/**
 * GET /api/documents/{id}
 * @returns {Promise<DocumentResponse>}
 */
export function getDocumentById(id) {
  return client.get(`/api/documents/${id}`).then((r) => r.data);
}

/**
 * DELETE /api/documents/{id}
 */
export function deleteDocument(id) {
  return client.delete(`/api/documents/${id}`).then((r) => r.data);
}

/**
 * Returns the full download URL for a document (authenticated endpoint).
 */
export function getDownloadUrl(id) {
  return `${API_BASE_URL}/api/documents/${id}/download`;
}
