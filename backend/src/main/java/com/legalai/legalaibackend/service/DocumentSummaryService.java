package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.DocumentSummaryResponse;

public interface DocumentSummaryService {

    /**
     * Generate or update the summary for a document.
     *
     * @param documentId Document ID
     * @return DocumentSummaryResponse
     */
    DocumentSummaryResponse generateSummary(Long documentId);

    /**
     * Get the existing summary for a document.
     *
     * @param documentId Document ID
     * @return DocumentSummaryResponse
     */
    DocumentSummaryResponse getSummary(Long documentId);
}