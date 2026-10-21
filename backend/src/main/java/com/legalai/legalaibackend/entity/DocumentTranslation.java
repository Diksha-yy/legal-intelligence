package com.legalai.legalaibackend.entity;

import jakarta.persistence.*;

import java.time.LocalDateTime;

@Entity
@Table(
        name = "document_translation",
        uniqueConstraints = {
                @UniqueConstraint(columnNames = "document_id")
        }
)
public class DocumentTranslation {

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
    @Column(name = "translated_text", columnDefinition = "LONGTEXT", nullable = false)
    private String translatedText;

    @Column(name = "source_language", nullable = false, length = 50)
    private String sourceLanguage;

    @Column(name = "target_language", nullable = false, length = 50)
    private String targetLanguage;

    @Column(name = "translation_model", nullable = false, length = 100)
    private String translationModel;

    @Column(name = "translated_at", nullable = false)
    private LocalDateTime translatedAt;

    public DocumentTranslation() {
    }

    @PrePersist
    public void prePersist() {
        if (translatedAt == null) {
            translatedAt = LocalDateTime.now();
        }
    }

    @PreUpdate
    public void preUpdate() {
        translatedAt = LocalDateTime.now();
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

    public String getTranslatedText() {
        return translatedText;
    }

    public void setTranslatedText(String translatedText) {
        this.translatedText = translatedText;
    }

    public String getSourceLanguage() {
        return sourceLanguage;
    }

    public void setSourceLanguage(String sourceLanguage) {
        this.sourceLanguage = sourceLanguage;
    }

    public String getTargetLanguage() {
        return targetLanguage;
    }

    public void setTargetLanguage(String targetLanguage) {
        this.targetLanguage = targetLanguage;
    }

    public String getTranslationModel() {
        return translationModel;
    }

    public void setTranslationModel(String translationModel) {
        this.translationModel = translationModel;
    }

    public LocalDateTime getTranslatedAt() {
        return translatedAt;
    }

    public void setTranslatedAt(LocalDateTime translatedAt) {
        this.translatedAt = translatedAt;
    }
}