package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.MissingClauseResponse;
import com.legalai.legalaibackend.entity.Clause;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.DocumentType;
import com.legalai.legalaibackend.entity.MandatoryClause;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.repository.ClauseRepository;
import com.legalai.legalaibackend.repository.DocumentRepository;
import com.legalai.legalaibackend.repository.DocumentTypeRepository;
import com.legalai.legalaibackend.repository.MandatoryClauseRepository;
import com.legalai.legalaibackend.service.MissingClauseService;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@Service
public class MissingClauseServiceImpl implements MissingClauseService {

    private final DocumentRepository documentRepository;
    private final ClauseRepository clauseRepository;
    private final DocumentTypeRepository documentTypeRepository;
    private final MandatoryClauseRepository mandatoryClauseRepository;

    public MissingClauseServiceImpl(
            DocumentRepository documentRepository,
            ClauseRepository clauseRepository,
            DocumentTypeRepository documentTypeRepository,
            MandatoryClauseRepository mandatoryClauseRepository) {

        this.documentRepository = documentRepository;
        this.clauseRepository = clauseRepository;
        this.documentTypeRepository = documentTypeRepository;
        this.mandatoryClauseRepository = mandatoryClauseRepository;
    }

    @Override
    public MissingClauseResponse detectMissingClauses(
            Long documentId,
            Long documentTypeId) {

        Document document = documentRepository.findById(documentId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id: " + documentId));

        DocumentType documentType = documentTypeRepository.findById(documentTypeId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document type not found with id: " + documentTypeId));

        List<MandatoryClause> mandatoryClauses =
                mandatoryClauseRepository.findByDocumentType(documentType);

        List<Clause> extractedClauses =
                clauseRepository.findByDocumentId(documentId);

        Set<String> detectedClauseNames = new HashSet<>();

        for (Clause clause : extractedClauses) {

            if (clause.getClauseName() != null &&
                    !clause.getClauseName().isBlank()) {

                detectedClauseNames.add(
                        normalize(clause.getClauseName())
                );
            }
        }

        List<String> missingClauses = new ArrayList<>();

        for (MandatoryClause mandatoryClause : mandatoryClauses) {

            String expected = normalize(
                    mandatoryClause.getClauseName());

            if (!detectedClauseNames.contains(expected)) {
                missingClauses.add(
                        mandatoryClause.getClauseName());
            }
        }

        MissingClauseResponse response = new MissingClauseResponse();

        response.setDocumentId(document.getId());
        response.setDocumentType(documentType.getName());
        response.setTotalMandatoryClauses(mandatoryClauses.size());
        response.setDetectedClauses(extractedClauses.size());
        response.setMissingCount(missingClauses.size());
        response.setMissingClauses(missingClauses);

        return response;
    }

    /**
     * Normalize clause names before comparison.
     * This helps OCR and AI outputs match correctly.
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