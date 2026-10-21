package com.legalai.legalaibackend.dto;

import java.time.LocalDateTime;

public class DocumentSummaryResponse {

    private Long id;
    private Long documentId;
    private String documentTitle;
    private String summary;
    private String summaryModel;
    private LocalDateTime generatedAt;

    public DocumentSummaryResponse() {
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getDocumentId() {
        return documentId;
    }

    public void setDocumentId(Long documentId) {
        this.documentId = documentId;
    }

    public String getDocumentTitle() {
        return documentTitle;
    }

    public void setDocumentTitle(String documentTitle) {
        this.documentTitle = documentTitle;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public String getSummaryModel() {
        return summaryModel;
    }

    public void setSummaryModel(String summaryModel) {
        this.summaryModel = summaryModel;
    }

    public LocalDateTime getGeneratedAt() {
        return generatedAt;
    }

    public void setGeneratedAt(LocalDateTime generatedAt) {
        this.generatedAt = generatedAt;
    }

    @Override
    public String toString() {
        return "DocumentSummaryResponse{" +
                "id=" + id +
                ", documentId=" + documentId +
                ", documentTitle='" + documentTitle + '\'' +
                ", summary='" + summary + '\'' +
                ", summaryModel='" + summaryModel + '\'' +
                ", generatedAt=" + generatedAt +
                '}';
    }
}