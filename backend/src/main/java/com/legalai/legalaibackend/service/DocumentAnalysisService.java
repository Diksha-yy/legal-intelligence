package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.DocumentAnalysisResponse;

import java.util.List;

public interface DocumentAnalysisService {

    /**
     * Analyze a document by comparing detected clauses
     * with mandatory clauses for the given document type.
     */
    DocumentAnalysisResponse analyzeDocument(
            String documentType,
            List<String> detectedClauses
    );

    /**
     * Returns only the missing clauses.
     * Used internally and can also be reused by other modules.
     */
    List<String> findMissingClauses(
            String documentType,
            List<String> detectedClauses
    );
}