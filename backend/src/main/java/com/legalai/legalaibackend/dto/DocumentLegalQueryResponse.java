package com.legalai.legalaibackend.dto;

import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

@Data
public class DocumentLegalQueryResponse {

    /**
     * Database ID of the Q&A record.
     */
    private Long id;

    /**
     * Document ID.
     */
    private Long documentId;

    /**
     * User's question.
     */
    private String question;

    /**
     * AI-generated grounded answer.
     */
    private String answer;

    /**
     * Retrieved clauses used to generate the answer.
     */
    private List<RetrievedClauseDTO> retrievedClauses;

    /**
     * Overall confidence score.
     */
    private Double confidenceScore;

    /**
     * Number of clauses retrieved.
     */
    private Integer retrievedClauseCount;

    /**
     * Embedding model used.
     */
    private String embeddingModel;

    /**
     * LLM used.
     */
    private String llmModel;

    /**
     * Timestamp.
     */
    private LocalDateTime createdAt;
}