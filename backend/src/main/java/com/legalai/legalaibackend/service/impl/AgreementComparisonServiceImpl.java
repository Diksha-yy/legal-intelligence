package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.AgreementComparisonRequest;
import com.legalai.legalaibackend.dto.AgreementComparisonResponse;
import com.legalai.legalaibackend.entity.AgreementComparison;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.enums.ComparisonStatus;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.mapper.AgreementComparisonMapper;
import com.legalai.legalaibackend.repository.AgreementComparisonRepository;
import com.legalai.legalaibackend.repository.DocumentRepository;
import com.legalai.legalaibackend.service.AgreementComparisonService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional
public class AgreementComparisonServiceImpl implements AgreementComparisonService {

    private final AgreementComparisonRepository comparisonRepository;
    private final DocumentRepository documentRepository;
    private final AgreementComparisonMapper mapper;

    @Override
    public AgreementComparisonResponse compareAgreements(
            AgreementComparisonRequest request) {

        Document versionA = documentRepository.findById(request.getVersionADocumentId())
                .orElseThrow(() ->
                        new ResourceNotFoundException("Version A document not found"));

        Document versionB = documentRepository.findById(request.getVersionBDocumentId())
                .orElseThrow(() ->
                        new ResourceNotFoundException("Version B document not found"));

        AgreementComparison comparison = new AgreementComparison();

        comparison.setVersionADocument(versionA);
        comparison.setVersionBDocument(versionB);

        comparison.setComparisonStatus(ComparisonStatus.PENDING);

        comparison.setComparisonSummary("Comparison request created successfully.");

        comparison.setComparisonModel("Pending AI Integration");

        comparison.setTotalClausesCompared(0);
        comparison.setMatchedClauses(0);
        comparison.setModifiedClauses(0);
        comparison.setAddedClauses(0);
        comparison.setRemovedClauses(0);

        comparison.setCreatedAt(LocalDateTime.now());
        comparison.setUpdatedAt(LocalDateTime.now());

        AgreementComparison saved = comparisonRepository.save(comparison);

        return mapper.toResponse(saved);
    }

    @Override
    @Transactional(readOnly = true)
    public AgreementComparisonResponse getComparisonById(Long comparisonId) {

        AgreementComparison comparison = comparisonRepository.findById(comparisonId)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Comparison not found"));

        return mapper.toResponse(comparison);
    }

    @Override
    @Transactional(readOnly = true)
    public List<AgreementComparisonResponse> getComparisonHistory(Long documentId) {

        return comparisonRepository
                .findByVersionADocumentIdOrVersionBDocumentId(documentId, documentId)
                .stream()
                .map(mapper::toResponse)
                .collect(Collectors.toList());
    }

    @Override
    public void deleteComparison(Long comparisonId) {

        AgreementComparison comparison = comparisonRepository.findById(comparisonId)
                .orElseThrow(() ->
                        new ResourceNotFoundException("Comparison not found"));

        comparisonRepository.delete(comparison);
    }
}