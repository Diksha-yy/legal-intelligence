package com.legalai.legalaibackend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class DocumentLegalQueryRequest {

    /**
     * Uploaded document ID.
     */
    @NotNull(message = "Document ID is required.")
    private Long documentId;

    /**
     * User's natural language question.
     */
    @NotBlank(message = "Question cannot be empty.")
    private String question;

    /**
     * Number of clauses to retrieve from FAISS.
     * Default = 5
     */
    private Integer topK = 5;

    /**
     * Optional conversation/session ID.
     * Enables multi-turn conversations later.
     */
    private String sessionId;
}