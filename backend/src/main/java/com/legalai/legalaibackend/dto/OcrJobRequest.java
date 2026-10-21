package com.legalai.legalaibackend.dto;

public class OcrJobRequest {

    private Long documentId;
    private String engine;

    public OcrJobRequest() {
    }

    public Long getDocumentId() {
        return documentId;
    }

    public void setDocumentId(Long documentId) {
        this.documentId = documentId;
    }

    public String getEngine() {
        return engine;
    }

    public void setEngine(String engine) {
        this.engine = engine;
    }
}