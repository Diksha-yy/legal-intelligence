package com.legalai.legalaibackend.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public class FairnessScoreRequest {

    @NotNull(message = "Document ID is required.")
    private Long documentId;

    @NotNull(message = "Fairness score is required.")
    @Min(value = 0, message = "Fairness score cannot be less than 0.")
    @Max(value = 100, message = "Fairness score cannot be greater than 100.")
    private Double fairnessScore;

    @Min(value = 0, message = "Rights count cannot be negative.")
    private Integer rightsPartyA = 0;

    @Min(value = 0, message = "Rights count cannot be negative.")
    private Integer rightsPartyB = 0;

    @Min(value = 0, message = "Obligations count cannot be negative.")
    private Integer obligationsPartyA = 0;

    @Min(value = 0, message = "Obligations count cannot be negative.")
    private Integer obligationsPartyB = 0;

    @Min(value = 0, message = "Penalties count cannot be negative.")
    private Integer penaltiesPartyA = 0;

    @Min(value = 0, message = "Penalties count cannot be negative.")
    private Integer penaltiesPartyB = 0;

    private String explanation;

    public FairnessScoreRequest() {
    }

    public Long getDocumentId() {
        return documentId;
    }

    public void setDocumentId(Long documentId) {
        this.documentId = documentId;
    }

    public Double getFairnessScore() {
        return fairnessScore;
    }

    public void setFairnessScore(Double fairnessScore) {
        this.fairnessScore = fairnessScore;
    }

    public Integer getRightsPartyA() {
        return rightsPartyA;
    }

    public void setRightsPartyA(Integer rightsPartyA) {
        this.rightsPartyA = rightsPartyA;
    }

    public Integer getRightsPartyB() {
        return rightsPartyB;
    }

    public void setRightsPartyB(Integer rightsPartyB) {
        this.rightsPartyB = rightsPartyB;
    }

    public Integer getObligationsPartyA() {
        return obligationsPartyA;
    }

    public void setObligationsPartyA(Integer obligationsPartyA) {
        this.obligationsPartyA = obligationsPartyA;
    }

    public Integer getObligationsPartyB() {
        return obligationsPartyB;
    }

    public void setObligationsPartyB(Integer obligationsPartyB) {
        this.obligationsPartyB = obligationsPartyB;
    }

    public Integer getPenaltiesPartyA() {
        return penaltiesPartyA;
    }

    public void setPenaltiesPartyA(Integer penaltiesPartyA) {
        this.penaltiesPartyA = penaltiesPartyA;
    }

    public Integer getPenaltiesPartyB() {
        return penaltiesPartyB;
    }

    public void setPenaltiesPartyB(Integer penaltiesPartyB) {
        this.penaltiesPartyB = penaltiesPartyB;
    }

    public String getExplanation() {
        return explanation;
    }

    public void setExplanation(String explanation) {
        this.explanation = explanation;
    }
}