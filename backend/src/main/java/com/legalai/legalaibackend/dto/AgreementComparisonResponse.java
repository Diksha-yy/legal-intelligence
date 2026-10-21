package com.legalai.legalaibackend.dto;

import com.legalai.legalaibackend.enums.ComparisonStatus;
import lombok.*;

import java.time.LocalDateTime;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class AgreementComparisonResponse {

    private Long id;

    private Long versionADocumentId;

    private Long versionBDocumentId;

    private String comparisonSummary;

    private Integer totalClausesCompared;

    private Integer matchedClauses;

    private Integer modifiedClauses;

    private Integer addedClauses;

    private Integer removedClauses;

    private String comparisonModel;

    private ComparisonStatus comparisonStatus;

    private List<ClauseDifferenceDTO> clauseDifferences;

    private LocalDateTime createdAt;

    private LocalDateTime updatedAt;

}