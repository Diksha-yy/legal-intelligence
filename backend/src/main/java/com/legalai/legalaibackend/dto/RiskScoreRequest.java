package com.legalai.legalaibackend.dto;

import jakarta.validation.constraints.NotNull;

public class RiskScoreRequest {

    @NotNull(message = "Document ID is required")
    private Long documentId;

    public RiskScoreRequest() {
    }

    public RiskScoreRequest(Long documentId) {
        this.documentId = documentId;
    }

    public Long getDocumentId() {
        return documentId;
    }

    public void setDocumentId(Long documentId) {
        this.documentId = documentId;
    }
}