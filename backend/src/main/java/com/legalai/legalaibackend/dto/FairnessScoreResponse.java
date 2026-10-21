package com.legalai.legalaibackend.dto;

import java.time.LocalDateTime;

public class FairnessScoreResponse {

    private Long id;

    private Long documentId;

    private Double fairnessScore;

    private Integer rightsPartyA;

    private Integer rightsPartyB;

    private Integer obligationsPartyA;

    private Integer obligationsPartyB;

    private Integer penaltiesPartyA;

    private Integer penaltiesPartyB;

    private String explanation;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

    public FairnessScoreResponse() {
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

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }
}