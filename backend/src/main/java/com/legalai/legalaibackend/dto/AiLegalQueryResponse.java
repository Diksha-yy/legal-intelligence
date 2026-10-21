package com.legalai.legalaibackend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AiLegalQueryResponse {

    /**
     * AI-generated answer.
     */
    private String answer;

    /**
     * Confidence score (0.0 - 1.0).
     */
    private Double confidenceScore;

    /**
     * Main source clause.
     */
    private String sourceClause;

    /**
     * Clauses retrieved by the RAG pipeline.
     */
    private List<RetrievedClauseDTO> retrievedClauses;

    /**
     * AI model name.
     */
    private String llmModel;

    /**
     * Embedding model used.
     */
    private String embeddingModel;
}