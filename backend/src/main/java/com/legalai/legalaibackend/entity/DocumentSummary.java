package com.legalai.legalaibackend.entity;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(
        name = "document_summary",
        uniqueConstraints = {
                @UniqueConstraint(columnNames = "document_id")
        }
)
public class DocumentSummary {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(
            name = "document_id",
            nullable = false,
            unique = true
    )
    private Document document;

    @Lob
    @Column(name = "summary", columnDefinition = "LONGTEXT", nullable = false)
    private String summary;

    @Column(name = "summary_model", nullable = false, length = 100)
    private String summaryModel;

    @Column(name = "generated_at", nullable = false)
    private LocalDateTime generatedAt;

    public DocumentSummary() {
    }

    @PrePersist
    public void prePersist() {
        if (generatedAt == null) {
            generatedAt = LocalDateTime.now();
        }
    }

    @PreUpdate
    public void preUpdate() {
        generatedAt = LocalDateTime.now();
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
}