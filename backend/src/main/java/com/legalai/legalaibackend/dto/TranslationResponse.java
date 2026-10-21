package com.legalai.legalaibackend.dto;

import java.time.LocalDateTime;

public class TranslationResponse {

    private Long id;
    private Long documentId;
    private String translatedText;
    private String targetLanguage;
    private String translationModel;
    private LocalDateTime translatedAt;

    public TranslationResponse() {
    }

    public TranslationResponse(Long id,
                               Long documentId,
                               String translatedText,
                               String targetLanguage,
                               String translationModel,
                               LocalDateTime translatedAt) {
        this.id = id;
        this.documentId = documentId;
        this.translatedText = translatedText;
        this.targetLanguage = targetLanguage;
        this.translationModel = translationModel;
        this.translatedAt = translatedAt;
    }

    public Long getId() {
        return id;
    }

    public Long getDocumentId() {
        return documentId;
    }

    public String getTranslatedText() {
        return translatedText;
    }

    public String getTargetLanguage() {
        return targetLanguage;
    }

    public String getTranslationModel() {
        return translationModel;
    }

    public LocalDateTime getTranslatedAt() {
        return translatedAt;
    }
}