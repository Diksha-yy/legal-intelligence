package com.legalai.legalaibackend.mapper;

import com.legalai.legalaibackend.dto.DocumentLegalQueryRequest;
import com.legalai.legalaibackend.dto.DocumentLegalQueryResponse;
import com.legalai.legalaibackend.dto.RetrievedClauseDTO;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.DocumentLegalQuery;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class DocumentLegalQueryMapper {

    /**
     * Request DTO -> Entity
     */
    public DocumentLegalQuery toEntity(
            DocumentLegalQueryRequest request,
            Document document) {

        DocumentLegalQuery entity = new DocumentLegalQuery();

        entity.setDocument(document);
        entity.setQuestion(request.getQuestion());

        // Will be updated by RAG later
        entity.setAnswer("");
        entity.setSourceClause("");
        entity.setConfidenceScore(0.0);
        entity.setRetrievedClauseCount(0);
        entity.setEmbeddingModel("all-MiniLM-L6-v2");
        entity.setLlmModel("Not Executed");

        return entity;
    }

    /**
     * Entity -> Response DTO
     */
    public DocumentLegalQueryResponse toResponse(
            DocumentLegalQuery entity,
            List<RetrievedClauseDTO> retrievedClauses) {

        DocumentLegalQueryResponse response =
                new DocumentLegalQueryResponse();

        response.setId(entity.getId());
        response.setDocumentId(entity.getDocument().getId());
        response.setQuestion(entity.getQuestion());
        response.setAnswer(entity.getAnswer());

        response.setRetrievedClauses(retrievedClauses);

        response.setConfidenceScore(entity.getConfidenceScore());
        response.setRetrievedClauseCount(entity.getRetrievedClauseCount());

        response.setEmbeddingModel(entity.getEmbeddingModel());
        response.setLlmModel(entity.getLlmModel());

        response.setCreatedAt(entity.getCreatedAt());

        return response;
    }
}