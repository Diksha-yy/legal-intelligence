package com.legalai.legalaibackend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RiskScoreResponse {

    private Long documentId;

    private Integer riskScore;

    private String riskLevel;

    private List<RiskFactorDTO> riskFactors;

    private String message;
}