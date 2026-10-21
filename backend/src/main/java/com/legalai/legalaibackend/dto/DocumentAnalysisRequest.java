package com.legalai.legalaibackend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;

import java.util.List;

public class DocumentAnalysisRequest {

    @NotBlank(message = "Document type is required")
    private String documentType;

    @NotEmpty(message = "Detected clauses cannot be empty")
    private List<String> detectedClauses;

    public DocumentAnalysisRequest() {
    }

    public DocumentAnalysisRequest(String documentType, List<String> detectedClauses) {
        this.documentType = documentType;
        this.detectedClauses = detectedClauses;
    }

    public String getDocumentType() {
        return documentType;
    }

    public void setDocumentType(String documentType) {
        this.documentType = documentType;
    }

    public List<String> getDetectedClauses() {
        return detectedClauses;
    }

    public void setDetectedClauses(List<String> detectedClauses) {
        this.detectedClauses = detectedClauses;
    }
}