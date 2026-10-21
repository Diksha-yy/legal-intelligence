package com.legalai.legalaibackend.entity;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "extracted_text")
public class ExtractedText {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Lob
    @Column(nullable = false, columnDefinition = "LONGTEXT")
    private String extractedText;

    @Column(nullable = false)
    private String extractionEngine;

    @Column(nullable = false)
    private Double confidence;

    @Column(nullable = false)
    private LocalDateTime extractedAt;

    @OneToOne
    @JoinColumn(name = "document_id", nullable = false)
    private Document document;

    public ExtractedText() {
    }

    public Long getId() {
        return id;
    }

    public String getExtractedText() {
        return extractedText;
    }

    public void setExtractedText(String extractedText) {
        this.extractedText = extractedText;
    }

    public String getExtractionEngine() {
        return extractionEngine;
    }

    public void setExtractionEngine(String extractionEngine) {
        this.extractionEngine = extractionEngine;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }

    public LocalDateTime getExtractedAt() {
        return extractedAt;
    }

    public void setExtractedAt(LocalDateTime extractedAt) {
        this.extractedAt = extractedAt;
    }

    public Document getDocument() {
        return document;
    }

    public void setDocument(Document document) {
        this.document = document;
    }
}