package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.DocumentLegalQueryRequest;
import com.legalai.legalaibackend.dto.DocumentLegalQueryResponse;

import java.util.List;

public interface DocumentLegalQueryService {

    /**
     * Ask a question about a document.
     * Executes the complete RAG pipeline.
     */
    DocumentLegalQueryResponse askQuestion(DocumentLegalQueryRequest request);

    /**
     * Get complete Q&A history for a document.
     */
    List<DocumentLegalQueryResponse> getQuestionHistory(Long documentId);

    /**
     * Get a single Q&A by its ID.
     */
    DocumentLegalQueryResponse getQuestionById(Long queryId);

    /**
     * Delete a single Q&A.
     */
    void deleteQuestion(Long queryId);

    /**
     * Delete all Q&A history of a document.
     */
    void deleteDocumentHistory(Long documentId);
}