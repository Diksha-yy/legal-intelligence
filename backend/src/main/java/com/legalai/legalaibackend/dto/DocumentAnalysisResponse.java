package com.legalai.legalaibackend.dto;

import java.util.List;

public class DocumentAnalysisResponse {

    private String documentType;

    private int totalMandatoryClauses;

    private int detectedClauses;

    private int missingClausesCount;

    private List<String> missingClauses;

    private boolean documentComplete;

    public DocumentAnalysisResponse() {
    }

    public DocumentAnalysisResponse(String documentType,
                                    int totalMandatoryClauses,
                                    int detectedClauses,
                                    int missingClausesCount,
                                    List<String> missingClauses,
                                    boolean documentComplete) {
        this.documentType = documentType;
        this.totalMandatoryClauses = totalMandatoryClauses;
        this.detectedClauses = detectedClauses;
        this.missingClausesCount = missingClausesCount;
        this.missingClauses = missingClauses;
        this.documentComplete = documentComplete;
    }

    public String getDocumentType() {
        return documentType;
    }

    public void setDocumentType(String documentType) {
        this.documentType = documentType;
    }

    public int getTotalMandatoryClauses() {
        return totalMandatoryClauses;
    }

    public void setTotalMandatoryClauses(int totalMandatoryClauses) {
        this.totalMandatoryClauses = totalMandatoryClauses;
    }

    public int getDetectedClauses() {
        return detectedClauses;
    }

    public void setDetectedClauses(int detectedClauses) {
        this.detectedClauses = detectedClauses;
    }

    public int getMissingClausesCount() {
        return missingClausesCount;
    }

    public void setMissingClausesCount(int missingClausesCount) {
        this.missingClausesCount = missingClausesCount;
    }

    public List<String> getMissingClauses() {
        return missingClauses;
    }

    public void setMissingClauses(List<String> missingClauses) {
        this.missingClauses = missingClauses;
    }

    public boolean isDocumentComplete() {
        return documentComplete;
    }

    public void setDocumentComplete(boolean documentComplete) {
        this.documentComplete = documentComplete;
    }
}