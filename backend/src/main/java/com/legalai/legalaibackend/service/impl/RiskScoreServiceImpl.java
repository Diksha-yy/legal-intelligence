package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.RiskFactorDTO;
import com.legalai.legalaibackend.dto.RiskScoreResponse;
import com.legalai.legalaibackend.engine.RiskRuleEngine;
import com.legalai.legalaibackend.entity.Clause;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.RiskScore;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.mapper.RiskScoreMapper;
import com.legalai.legalaibackend.repository.ClauseRepository;
import com.legalai.legalaibackend.repository.DocumentRepository;
import com.legalai.legalaibackend.repository.RiskScoreRepository;
import com.legalai.legalaibackend.service.RiskScoreService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
@RequiredArgsConstructor
public class RiskScoreServiceImpl implements RiskScoreService {

    private final DocumentRepository documentRepository;
    private final ClauseRepository clauseRepository;
    private final RiskRuleEngine riskRuleEngine;
    private final RiskScoreRepository riskScoreRepository;
    private final RiskScoreMapper riskScoreMapper;

    @Override
    public RiskScoreResponse calculateRiskScore(Long documentId) {

        Document document = documentRepository.findById(documentId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id: " + documentId));

        List<Clause> clauses = clauseRepository.findByDocumentId(documentId);

        List<RiskFactorDTO> riskFactors =
                riskRuleEngine.calculateRiskFactors(clauses);

        int totalScore =
                riskRuleEngine.calculateTotalScore(riskFactors);

        String riskLevel =
                riskRuleEngine.determineRiskLevel(totalScore);

        RiskScore riskScore = riskScoreRepository
                .findByDocumentId(documentId)
                .orElseGet(() -> {
                    RiskScore rs = new RiskScore();
                    rs.setDocument(document);
                    return rs;
                });

        riskScore.setRiskScore(totalScore);
        riskScore.setRiskLevel(riskLevel);
        riskScore.setUpdatedAt(LocalDateTime.now());

        RiskScore savedRiskScore = riskScoreRepository.save(riskScore);

        return riskScoreMapper.toResponse(
                savedRiskScore,
                riskFactors,
                "Risk Score calculated successfully."
        );
    }
}