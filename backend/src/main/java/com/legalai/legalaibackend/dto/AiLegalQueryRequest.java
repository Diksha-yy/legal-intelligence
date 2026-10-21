package com.legalai.legalaibackend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AiLegalQueryRequest {

    @NotNull(message = "Document ID is required.")
    private Long documentId;

    @NotBlank(message = "Question is required.")
    private String question;
}