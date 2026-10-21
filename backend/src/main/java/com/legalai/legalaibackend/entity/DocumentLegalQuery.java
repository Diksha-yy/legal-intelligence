package com.legalai.legalaibackend.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "document_legal_queries")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class DocumentLegalQuery {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /**
     * Uploaded document for which the question is asked.
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "document_id", nullable = false)
    private Document document;

    /**
     * User's natural language question.
     */
    @Column(nullable = false, columnDefinition = "TEXT")
    private String question;

    /**
     * AI-generated answer.
     */
    @Column(nullable = false, columnDefinition = "TEXT")
    private String answer;

    /**
     * Source clause(s) retrieved from the document.
     * Example:
     * Clause 5
     * Clause 8
     * Clause 10
     */
    @Column(name = "source_clause", columnDefinition = "TEXT")
    private String sourceClause;

    /**
     * Similarity / confidence score.
     */
    @Column(name = "confidence_score")
    private Double confidenceScore;

    /**
     * Number of clauses retrieved from FAISS.
     */
    @Column(name = "retrieved_clause_count")
    private Integer retrievedClauseCount;

    /**
     * Name of embedding model used.
     * Example:
     * all-MiniLM-L6-v2
     */
    @Column(name = "embedding_model")
    private String embeddingModel;

    /**
     * Name of LLM used.
     * Example:
     * Ollama
     * OpenAI
     * Gemini
     */
    @Column(name = "llm_model")
    private String llmModel;

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    public void prePersist() {
        LocalDateTime now = LocalDateTime.now();
        this.createdAt = now;
        this.updatedAt = now;
    }

    @PreUpdate
    public void preUpdate() {
        this.updatedAt = LocalDateTime.now();
    }
}