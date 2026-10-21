package com.legalai.legalaibackend.entity;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "fairness_scores")
public class FairnessScore {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(
            name = "document_id",
            nullable = false,
            unique = true
    )
    private Document document;

    @Column(name = "fairness_score", nullable = false)
    private Double fairnessScore;

    @Column(name = "rights_party_a")
    private Integer rightsPartyA = 0;

    @Column(name = "rights_party_b")
    private Integer rightsPartyB = 0;

    @Column(name = "obligations_party_a")
    private Integer obligationsPartyA = 0;

    @Column(name = "obligations_party_b")
    private Integer obligationsPartyB = 0;

    @Column(name = "penalties_party_a")
    private Integer penaltiesPartyA = 0;

    @Column(name = "penalties_party_b")
    private Integer penaltiesPartyB = 0;

    @Column(columnDefinition = "TEXT")
    private String explanation;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;

    public FairnessScore() {
    }

    @PrePersist
    public void onCreate() {
        LocalDateTime now = LocalDateTime.now();
        this.createdAt = now;
        this.updatedAt = now;
    }

    @PreUpdate
    public void onUpdate() {
        this.updatedAt = LocalDateTime.now();
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

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
}