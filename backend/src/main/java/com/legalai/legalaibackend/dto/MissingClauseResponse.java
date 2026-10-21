package com.legalai.legalaibackend.dto;

import java.util.List;

public class MissingClauseResponse {

    private Long documentId;

    private String documentType;

    private Integer totalMandatoryClauses;

    private Integer detectedClauses;

    private Integer missingCount;

    private List<String> missingClauses;

    public MissingClauseResponse() {
    }

    public MissingClauseResponse(Long documentId,
                                 String documentType,
                                 Integer totalMandatoryClauses,
                                 Integer detectedClauses,
                                 Integer missingCount,
                                 List<String> missingClauses) {
        this.documentId = documentId;
        this.documentType = documentType;
        this.totalMandatoryClauses = totalMandatoryClauses;
        this.detectedClauses = detectedClauses;
        this.missingCount = missingCount;
        this.missingClauses = missingClauses;
    }

    public Long getDocumentId() {
        return documentId;
    }

    public void setDocumentId(Long documentId) {
        this.documentId = documentId;
    }

    public String getDocumentType() {
        return documentType;
    }

    public void setDocumentType(String documentType) {
        this.documentType = documentType;
    }

    public Integer getTotalMandatoryClauses() {
        return totalMandatoryClauses;
    }

    public void setTotalMandatoryClauses(Integer totalMandatoryClauses) {
        this.totalMandatoryClauses = totalMandatoryClauses;
    }

    public Integer getDetectedClauses() {
        return detectedClauses;
    }

    public void setDetectedClauses(Integer detectedClauses) {
        this.detectedClauses = detectedClauses;
    }

    public Integer getMissingCount() {
        return missingCount;
    }

    public void setMissingCount(Integer missingCount) {
        this.missingCount = missingCount;
    }

    public List<String> getMissingClauses() {
        return missingClauses;
    }

    public void setMissingClauses(List<String> missingClauses) {
        this.missingClauses = missingClauses;
    }
}