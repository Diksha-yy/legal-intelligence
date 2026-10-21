package com.legalai.legalaibackend.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "mandatory_clauses")
public class MandatoryClause {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String clauseName;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "document_type_id", nullable = false)
    private DocumentType documentType;

    @Column(columnDefinition = "TEXT")
    private String description;

    public MandatoryClause() {
    }

    public MandatoryClause(Long id,
                           String clauseName,
                           DocumentType documentType,
                           String description) {
        this.id = id;
        this.clauseName = clauseName;
        this.documentType = documentType;
        this.description = description;
    }

    public Long getId() {
        return id;
    }

    public String getClauseName() {
        return clauseName;
    }

    public void setClauseName(String clauseName) {
        this.clauseName = clauseName;
    }

    public DocumentType getDocumentType() {
        return documentType;
    }

    public void setDocumentType(DocumentType documentType) {
        this.documentType = documentType;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}