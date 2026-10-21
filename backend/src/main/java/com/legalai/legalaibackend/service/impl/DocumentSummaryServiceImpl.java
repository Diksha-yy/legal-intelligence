package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.DocumentSummaryResponse;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.DocumentSummary;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.repository.DocumentRepository;
import com.legalai.legalaibackend.repository.DocumentSummaryRepository;
import com.legalai.legalaibackend.service.DocumentSummaryService;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class DocumentSummaryServiceImpl implements DocumentSummaryService {

    private final DocumentRepository documentRepository;
    private final DocumentSummaryRepository summaryRepository;

    public DocumentSummaryServiceImpl(
            DocumentRepository documentRepository,
            DocumentSummaryRepository summaryRepository) {
        this.documentRepository = documentRepository;
        this.summaryRepository = summaryRepository;
    }

    @Override
    public DocumentSummaryResponse generateSummary(Long documentId) {

        Document document = documentRepository.findById(documentId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id: " + documentId));

        // TODO: Replace this with actual AI summary generation
        String summaryText =
                "This is a mock AI-generated summary for the uploaded document.";

        // Update existing summary instead of creating duplicates
        DocumentSummary summary = summaryRepository
                .findByDocument(document)
                .orElse(new DocumentSummary());

        summary.setDocument(document);
        summary.setSummary(summaryText);
        summary.setSummaryModel("Mock AI");
        summary.setGeneratedAt(LocalDateTime.now());

        summary = summaryRepository.save(summary);

        return mapToResponse(summary);
    }

    @Override
    public DocumentSummaryResponse getSummary(Long documentId) {

        Document document = documentRepository.findById(documentId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id: " + documentId));

        DocumentSummary summary = summaryRepository
                .findByDocument(document)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Summary not found for document id: " + documentId));

        return mapToResponse(summary);
    }

    private DocumentSummaryResponse mapToResponse(DocumentSummary summary) {

        DocumentSummaryResponse response = new DocumentSummaryResponse();

        response.setId(summary.getId());
        response.setDocumentId(summary.getDocument().getId());
        response.setDocumentTitle(summary.getDocument().getTitle());
        response.setSummary(summary.getSummary());
        response.setSummaryModel(summary.getSummaryModel());
        response.setGeneratedAt(summary.getGeneratedAt());

        return response;
    }
}