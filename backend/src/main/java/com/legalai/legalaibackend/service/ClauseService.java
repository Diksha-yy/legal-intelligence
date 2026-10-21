package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.ClauseRequest;
import com.legalai.legalaibackend.dto.ClauseResponse;
import com.legalai.legalaibackend.entity.Clause;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.repository.ClauseRepository;
import com.legalai.legalaibackend.repository.DocumentRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ClauseService {

    private final ClauseRepository clauseRepository;
    private final DocumentRepository documentRepository;

    public ClauseService(ClauseRepository clauseRepository,
                         DocumentRepository documentRepository) {
        this.clauseRepository = clauseRepository;
        this.documentRepository = documentRepository;
    }

    public ClauseResponse saveClause(ClauseRequest request) {

        Document document = documentRepository.findById(request.getDocumentId())
                .orElseThrow(() -> new RuntimeException("Document not found"));

        Clause clause = new Clause();
        clause.setClauseText(request.getClauseText());
        if (request.getClauseName() == null ||
                request.getClauseName().isBlank()) {

            throw new RuntimeException("Clause Name is required.");
        }

        clause.setClauseName(
                request.getClauseName()
                        .trim()
                        .toUpperCase()
        );
        clause.setConfidence(request.getConfidence());
        clause.setCreatedAt(LocalDateTime.now());
        clause.setDocument(document);

        Clause saved = clauseRepository.save(clause);

        return mapToResponse(saved);
    }

    public List<ClauseResponse> getAllClauses() {
        return clauseRepository.findAll()
                .stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    public List<ClauseResponse> getClausesByDocument(Long documentId) {

        return clauseRepository.findByDocumentId(documentId)
                .stream()
                .map(this::mapToResponse)
                .collect(Collectors.toList());
    }

    private ClauseResponse mapToResponse(Clause clause) {

        ClauseResponse response = new ClauseResponse();

        response.setId(clause.getId());
        response.setClauseText(clause.getClauseText());
        response.setClauseName(clause.getClauseName());
        response.setConfidence(clause.getConfidence());
        response.setCreatedAt(clause.getCreatedAt());
        response.setDocumentId(clause.getDocument().getId());

        return response;
    }
}