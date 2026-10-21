package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.RiskScoreResponse;

public interface RiskScoreService {

    /**
     * Calculate risk score for a document.
     *
     * @param documentId ID of the uploaded document
     * @return RiskScoreResponse
     */
    RiskScoreResponse calculateRiskScore(Long documentId);
}