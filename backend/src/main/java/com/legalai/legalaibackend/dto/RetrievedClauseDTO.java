package com.legalai.legalaibackend.dto;

import lombok.Data;

@Data
public class RetrievedClauseDTO {

    /**
     * Clause ID from database.
     */
    private Long clauseId;

    /**
     * Clause number.
     * Example:
     * Clause 5
     * Section 3.2
     */
    private String clauseNumber;

    /**
     * Retrieved clause text.
     */
    private String clauseText;

    /**
     * Similarity score from vector search.
     */
    private Double similarityScore;

    /**
     * Start page in document.
     */
    private Integer pageNumber;
}