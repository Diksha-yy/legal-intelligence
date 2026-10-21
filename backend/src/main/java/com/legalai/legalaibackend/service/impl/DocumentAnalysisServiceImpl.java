package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.DocumentAnalysisResponse;
import com.legalai.legalaibackend.entity.DocumentType;
import com.legalai.legalaibackend.entity.MandatoryClause;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.repository.DocumentTypeRepository;
import com.legalai.legalaibackend.repository.MandatoryClauseRepository;
import com.legalai.legalaibackend.service.DocumentAnalysisService;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

@Service
public class DocumentAnalysisServiceImpl implements DocumentAnalysisService {

    private final DocumentTypeRepository documentTypeRepository;
    private final MandatoryClauseRepository mandatoryClauseRepository;

    public DocumentAnalysisServiceImpl(
            DocumentTypeRepository documentTypeRepository,
            MandatoryClauseRepository mandatoryClauseRepository) {

        this.documentTypeRepository = documentTypeRepository;
        this.mandatoryClauseRepository = mandatoryClauseRepository;
    }

    @Override
    public DocumentAnalysisResponse analyzeDocument(
            String documentTypeName,
            List<String> detectedClauses) {

        if (documentTypeName == null || documentTypeName.isBlank()) {
            throw new IllegalArgumentException("Document type is required.");
        }

        DocumentType documentType = documentTypeRepository
                .findByName(documentTypeName.trim())
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Document type not found: " + documentTypeName));

        List<MandatoryClause> mandatoryClauses =
                mandatoryClauseRepository.findByDocumentType(documentType);

        List<String> missingClauses =
                findMissingClauses(documentTypeName, detectedClauses);

        DocumentAnalysisResponse response = new DocumentAnalysisResponse();

        response.setDocumentType(documentType.getName());
        response.setTotalMandatoryClauses(mandatoryClauses.size());
        response.setDetectedClauses(
                detectedClauses == null ? 0 : detectedClauses.size());
        response.setMissingClausesCount(missingClauses.size());
        response.setMissingClauses(missingClauses);
        response.setDocumentComplete(missingClauses.isEmpty());

        return response;
    }

    @Override
    public List<String> findMissingClauses(
            String documentTypeName,
            List<String> detectedClauses) {

        if (documentTypeName == null || documentTypeName.isBlank()) {
            throw new IllegalArgumentException("Document type is required.");
        }

        DocumentType documentType = documentTypeRepository
                .findByName(documentTypeName.trim())
                .orElseThrow(() -> new ResourceNotFoundException(
                        "Document type not found: " + documentTypeName));

        List<MandatoryClause> mandatoryClauses =
                mandatoryClauseRepository.findByDocumentType(documentType);

        if (mandatoryClauses.isEmpty()) {
            return Collections.emptyList();
        }

        if (detectedClauses == null) {
            detectedClauses = Collections.emptyList();
        }

        List<String> missingClauses = new ArrayList<>();

        for (MandatoryClause mandatory : mandatoryClauses) {

            boolean found = detectedClauses.stream()
                    .filter(c -> c != null && !c.isBlank())
                    .map(this::normalize)
                    .anyMatch(c ->
                            c.equals(normalize(mandatory.getClauseName())));

            if (!found) {
                missingClauses.add(mandatory.getClauseName());
            }
        }

        return missingClauses;
    }

    /**
     * Normalizes clause names for reliable matching.
     */
    private String normalize(String text) {

        if (text == null) {
            return "";
        }

        return text.trim()
                .replaceAll("\\s+", " ")
                .replace("-", " ")
                .replace("_", " ")
                .toLowerCase();
    }
}