package com.legalai.legalaibackend.entity;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "risk_assessments")
public class RiskAssessment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "document_id", nullable = false, unique = true)
    private Document document;

    private Integer riskScore;

    private String riskLevel;

    @Column(columnDefinition = "TEXT")
    private String explanation;

    private Integer penaltyWeight;

    private Integer terminationWeight;

    private Integer paymentWeight;

    private Integer obligationWeight;

    private Integer missingClauseWeight;

    private LocalDateTime generatedAt;

    @PrePersist
    public void prePersist() {
        generatedAt = LocalDateTime.now();
    }

    public RiskAssessment() {
    }

    public Long getId() {
        return id;
    }

    public Document getDocument() {
        return document;
    }

    public void setDocument(Document document) {
        this.document = document;
    }

    public Integer getRiskScore() {
        return riskScore;
    }

    public void setRiskScore(Integer riskScore) {
        this.riskScore = riskScore;
    }

    public String getRiskLevel() {
        return riskLevel;
    }

    public void setRiskLevel(String riskLevel) {
        this.riskLevel = riskLevel;
    }

    public String getExplanation() {
        return explanation;
    }

    public void setExplanation(String explanation) {
        this.explanation = explanation;
    }

    public Integer getPenaltyWeight() {
        return penaltyWeight;
    }

    public void setPenaltyWeight(Integer penaltyWeight) {
        this.penaltyWeight = penaltyWeight;
    }

    public Integer getTerminationWeight() {
        return terminationWeight;
    }

    public void setTerminationWeight(Integer terminationWeight) {
        this.terminationWeight = terminationWeight;
    }

    public Integer getPaymentWeight() {
        return paymentWeight;
    }

    public void setPaymentWeight(Integer paymentWeight) {
        this.paymentWeight = paymentWeight;
    }

    public Integer getObligationWeight() {
        return obligationWeight;
    }

    public void setObligationWeight(Integer obligationWeight) {
        this.obligationWeight = obligationWeight;
    }

    public Integer getMissingClauseWeight() {
        return missingClauseWeight;
    }

    public void setMissingClauseWeight(Integer missingClauseWeight) {
        this.missingClauseWeight = missingClauseWeight;
    }

    public LocalDateTime getGeneratedAt() {
        return generatedAt;
    }
}