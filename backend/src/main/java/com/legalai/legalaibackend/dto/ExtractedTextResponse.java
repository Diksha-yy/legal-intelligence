package com.legalai.legalaibackend.dto;

import java.time.LocalDateTime;

public class ExtractedTextResponse {

    private Long id;
    private String extractedText;
    private String extractionEngine;
    private Double confidence;
    private LocalDateTime extractedAt;
    private Long documentId;

    public ExtractedTextResponse() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getExtractedText() {
        return extractedText;
    }

    public void setExtractedText(String extractedText) {
        this.extractedText = extractedText;
    }

    public String getExtractionEngine() {
        return extractionEngine;
    }

    public void setExtractionEngine(String extractionEngine) {
        this.extractionEngine = extractionEngine;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }

    public LocalDateTime getExtractedAt() {
        return extractedAt;
    }

    public void setExtractedAt(LocalDateTime extractedAt) {
        this.extractedAt = extractedAt;
    }

    public Long getDocumentId() {
        return documentId;
    }

    public void setDocumentId(Long documentId) {
        this.documentId = documentId;
    }
}