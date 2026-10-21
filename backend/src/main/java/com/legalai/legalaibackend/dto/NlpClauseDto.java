package com.legalai.legalaibackend.dto;

public class NlpClauseDto {

    private String clauseName;
    private String clauseText;
    private Double confidence;

    public NlpClauseDto() {
    }

    public NlpClauseDto(String clauseName, String clauseText, Double confidence) {
        this.clauseName = clauseName;
        this.clauseText = clauseText;
        this.confidence = confidence;
    }

    public String getClauseName() {
        return clauseName;
    }

    public void setClauseName(String clauseName) {
        this.clauseName = clauseName;
    }

    public String getClauseText() {
        return clauseText;
    }

    public void setClauseText(String clauseText) {
        this.clauseText = clauseText;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }
}