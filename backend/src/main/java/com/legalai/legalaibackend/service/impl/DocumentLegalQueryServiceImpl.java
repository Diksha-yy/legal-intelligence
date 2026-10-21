package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.AiLegalQueryRequest;
import com.legalai.legalaibackend.dto.AiLegalQueryResponse;
import com.legalai.legalaibackend.dto.DocumentLegalQueryRequest;
import com.legalai.legalaibackend.dto.DocumentLegalQueryResponse;
import com.legalai.legalaibackend.dto.RetrievedClauseDTO;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.DocumentLegalQuery;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.integration.AiServiceClient;
import com.legalai.legalaibackend.mapper.DocumentLegalQueryMapper;
import com.legalai.legalaibackend.repository.DocumentLegalQueryRepository;
import com.legalai.legalaibackend.repository.DocumentRepository;
import com.legalai.legalaibackend.service.DocumentLegalQueryService;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;

@Service
@Transactional
@RequiredArgsConstructor
public class DocumentLegalQueryServiceImpl
        implements DocumentLegalQueryService {

    private final DocumentRepository documentRepository;
    private final DocumentLegalQueryRepository documentLegalQueryRepository;
    private final DocumentLegalQueryMapper documentLegalQueryMapper;
    private final AiServiceClient aiServiceClient;

    @Override
    public DocumentLegalQueryResponse askQuestion(
            DocumentLegalQueryRequest request) {

        Document document = documentRepository.findById(request.getDocumentId())
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id : "
                                        + request.getDocumentId()));

        DocumentLegalQuery legalQuery =
                documentLegalQueryMapper.toEntity(request, document);

        AiLegalQueryRequest aiRequest =
                new AiLegalQueryRequest(
                        request.getDocumentId(),
                        request.getQuestion()
                );

        AiLegalQueryResponse aiResponse =
                aiServiceClient.askQuestion(aiRequest);

        legalQuery.setAnswer(aiResponse.getAnswer());
        legalQuery.setSourceClause(aiResponse.getSourceClause());

        legalQuery.setConfidenceScore(
                aiResponse.getConfidenceScore()
        );

        legalQuery.setEmbeddingModel(
                aiResponse.getEmbeddingModel()
        );

        legalQuery.setLlmModel(
                aiResponse.getLlmModel()
        );

        List<RetrievedClauseDTO> retrievedClauses =
                aiResponse.getRetrievedClauses();

        legalQuery.setRetrievedClauseCount(
                retrievedClauses == null ? 0 : retrievedClauses.size()
        );

        DocumentLegalQuery saved =
                documentLegalQueryRepository.save(legalQuery);

        return documentLegalQueryMapper.toResponse(
                saved,
                retrievedClauses == null
                        ? Collections.emptyList()
                        : retrievedClauses
        );
    }

    @Override
    public List<DocumentLegalQueryResponse> getQuestionHistory(
            Long documentId) {

        List<DocumentLegalQuery> queries =
                documentLegalQueryRepository
                        .findByDocumentIdOrderByCreatedAtDesc(documentId);

        return queries.stream()
                .map(query -> documentLegalQueryMapper.toResponse(
                        query,
                        Collections.emptyList()
                ))
                .toList();
    }

    @Override
    public DocumentLegalQueryResponse getQuestionById(
            Long queryId) {

        DocumentLegalQuery query =
                documentLegalQueryRepository.findById(queryId)
                        .orElseThrow(() ->
                                new ResourceNotFoundException(
                                        "Question not found."));

        return documentLegalQueryMapper.toResponse(
                query,
                Collections.emptyList()
        );
    }

    @Override
    public void deleteQuestion(Long queryId) {

        if (!documentLegalQueryRepository.existsById(queryId)) {
            throw new ResourceNotFoundException(
                    "Question not found.");
        }

        documentLegalQueryRepository.deleteById(queryId);
    }

    @Override
    public void deleteDocumentHistory(Long documentId) {

        documentLegalQueryRepository.deleteByDocumentId(documentId);
    }
}