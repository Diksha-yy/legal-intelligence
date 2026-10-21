package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.DocumentTranslationResponse;

public interface DocumentTranslationService {

    /**
     * Generate or update translation for a document.
     */
    DocumentTranslationResponse generateTranslation(Long documentId, String language);

    /**
     * Get existing translation for a document.
     */
    DocumentTranslationResponse getTranslation(Long documentId);
}