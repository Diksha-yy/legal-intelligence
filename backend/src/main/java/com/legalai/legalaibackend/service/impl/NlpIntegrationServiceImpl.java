package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.MissingClauseResponse;
import com.legalai.legalaibackend.entity.Clause;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.repository.ClauseRepository;
import com.legalai.legalaibackend.repository.DocumentRepository;
import com.legalai.legalaibackend.service.MissingClauseService;
import com.legalai.legalaibackend.service.NlpIntegrationService;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;

@Service
public class NlpIntegrationServiceImpl implements NlpIntegrationService {

    private final RestTemplate restTemplate;
    private final DocumentRepository documentRepository;
    private final ClauseRepository clauseRepository;
    private final MissingClauseService missingClauseService;

    @Value("${nlp.service.url}")
    private String nlpServiceUrl;

    public NlpIntegrationServiceImpl(
            RestTemplate restTemplate,
            DocumentRepository documentRepository,
            ClauseRepository clauseRepository,
            MissingClauseService missingClauseService) {

        this.restTemplate = restTemplate;
        this.documentRepository = documentRepository;
        this.clauseRepository = clauseRepository;
        this.missingClauseService = missingClauseService;
    }

    @Override
    public MissingClauseResponse analyzeDocument(
            Long documentId,
            Long documentTypeId) {

        Document document = documentRepository.findById(documentId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id: " + documentId));

        /*
         * MOCK MODE
         * Replace this section with Python NLP integration later.
         */

        if (clauseRepository.findByDocumentId(documentId).isEmpty()) {

            Clause clause = new Clause();
            clause.setDocument(document);
            clause.setClauseName("RENT");
            clause.setClauseText(
                    "Tenant shall pay rent before the 5th of every month.");
            clause.setConfidence(0.98);
            clause.setCreatedAt(LocalDateTime.now());

            clauseRepository.save(clause);
        }

        return missingClauseService.detectMissingClauses(
                documentId,
                documentTypeId);
    }

    /*
    ==========================================================
    FUTURE PYTHON / AI INTEGRATION

    NlpResponse response = restTemplate.postForObject(
            nlpServiceUrl,
            document,
            NlpResponse.class
    );

    if (response != null && response.getClauses() != null) {

        clauseRepository.deleteByDocument(document);

        for (NlpClauseDto dto : response.getClauses()) {

            Clause clause = new Clause();
            clause.setDocument(document);
            clause.setClauseName(dto.getClauseName());
            clause.setClauseText(dto.getClauseText());
            clause.setConfidence(dto.getConfidence());
            clause.setCreatedAt(LocalDateTime.now());

            clauseRepository.save(clause);
        }
    }

    return missingClauseService.detectMissingClauses(
            documentId,
            documentTypeId);

    ==========================================================
    */
}