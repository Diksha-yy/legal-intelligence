package com.legalai.legalaibackend.mapper;

import com.legalai.legalaibackend.dto.AgreementComparisonResponse;
import com.legalai.legalaibackend.entity.AgreementComparison;
import org.springframework.stereotype.Component;

import java.util.Collections;

@Component
public class AgreementComparisonMapper {

    public AgreementComparisonResponse toResponse(AgreementComparison entity) {

        if (entity == null) {
            return null;
        }

        return AgreementComparisonResponse.builder()
                .id(entity.getId())
                .versionADocumentId(
                        entity.getVersionADocument() != null
                                ? entity.getVersionADocument().getId()
                                : null
                )
                .versionBDocumentId(
                        entity.getVersionBDocument() != null
                                ? entity.getVersionBDocument().getId()
                                : null
                )
                .comparisonSummary(entity.getComparisonSummary())
                .totalClausesCompared(entity.getTotalClausesCompared())
                .matchedClauses(entity.getMatchedClauses())
                .modifiedClauses(entity.getModifiedClauses())
                .addedClauses(entity.getAddedClauses())
                .removedClauses(entity.getRemovedClauses())
                .comparisonModel(entity.getComparisonModel())
                .comparisonStatus(entity.getComparisonStatus())
                .createdAt(entity.getCreatedAt())
                .updatedAt(entity.getUpdatedAt())
                // AI service will populate this later
                .clauseDifferences(Collections.emptyList())
                .build();
    }

}