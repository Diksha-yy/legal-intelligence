package com.legalai.legalaibackend.dto;

import jakarta.validation.constraints.NotNull;
import lombok.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AgreementComparisonRequest {

    @NotNull(message = "Version A Document ID is required")
    private Long versionADocumentId;

    @NotNull(message = "Version B Document ID is required")
    private Long versionBDocumentId;

}