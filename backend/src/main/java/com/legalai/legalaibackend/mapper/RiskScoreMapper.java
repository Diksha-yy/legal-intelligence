package com.legalai.legalaibackend.mapper;

import com.legalai.legalaibackend.dto.RiskFactorDTO;
import com.legalai.legalaibackend.dto.RiskScoreResponse;
import com.legalai.legalaibackend.entity.RiskScore;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class RiskScoreMapper {

    public RiskScoreResponse toResponse(
            RiskScore riskScore,
            List<RiskFactorDTO> riskFactors,
            String message) {

        RiskScoreResponse response = new RiskScoreResponse();

        response.setDocumentId(riskScore.getDocument().getId());
        response.setRiskScore(riskScore.getRiskScore());
        response.setRiskLevel(riskScore.getRiskLevel());
        response.setRiskFactors(riskFactors);
        response.setMessage(message);

        return response;
    }
}