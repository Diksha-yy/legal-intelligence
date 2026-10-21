package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.OcrJobResponse;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.ExtractedText;
import com.legalai.legalaibackend.entity.OcrJob;
import com.legalai.legalaibackend.enums.DocumentStatus;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.repository.DocumentRepository;
import com.legalai.legalaibackend.repository.ExtractedTextRepository;
import com.legalai.legalaibackend.repository.OcrJobRepository;
import com.legalai.legalaibackend.service.OcrJobService;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class OcrJobServiceImpl implements OcrJobService {

    private final OcrJobRepository ocrJobRepository;
    private final DocumentRepository documentRepository;
    private final ExtractedTextRepository extractedTextRepository;

    public OcrJobServiceImpl(
            OcrJobRepository ocrJobRepository,
            DocumentRepository documentRepository,
            ExtractedTextRepository extractedTextRepository) {

        this.ocrJobRepository = ocrJobRepository;
        this.documentRepository = documentRepository;
        this.extractedTextRepository = extractedTextRepository;
    }

    @Override
    public OcrJobResponse startOcr(Long documentId) {

        Document document = documentRepository.findById(documentId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id: " + documentId));

        /*
         * Since one OCR Job exists per document,
         * reuse it instead of creating a new row.
         */
        OcrJob job = ocrJobRepository.findByDocument(document)
                .orElse(new OcrJob());

        if (job.getId() == null) {
            job.setDocument(document);
        }

        job.setStatus("PROCESSING");
        job.setStartedAt(LocalDateTime.now());

        job = ocrJobRepository.save(job);

        /*
         * Mock OCR
         * Replace this with Tesseract/AWS Textract/Google Vision later.
         */
        String extractedContent =
                "Sample OCR text extracted from uploaded document.";

        /*
         * Update existing ExtractedText if available.
         */
        ExtractedText extractedText = extractedTextRepository
                .findByDocument(document)
                .orElse(new ExtractedText());

        extractedText.setDocument(document);
        extractedText.setExtractedText(extractedContent);
        extractedText.setExtractionEngine("Mock OCR");
        extractedText.setConfidence(99.0);
        extractedText.setExtractedAt(LocalDateTime.now());

        extractedTextRepository.save(extractedText);

        /*
         * Finish OCR Job
         */
        job.setEngine("Mock OCR");
        job.setExtractedText(extractedContent);
        job.setStatus("COMPLETED");
        job.setCompletedAt(LocalDateTime.now());

        job = ocrJobRepository.save(job);

        /*
         * Update document status after OCR completes
         */
        document.setStatus(DocumentStatus.COMPLETED);
        documentRepository.save(document);

        return mapToResponse(job);
    }

    @Override
    public OcrJobResponse getLatestJob(Long documentId) {

        Document document = documentRepository.findById(documentId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id: " + documentId));

        OcrJob job = ocrJobRepository
                .findTopByDocumentOrderByCreatedAtDesc(document)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "OCR job not found for document id: "
                                        + documentId));

        return mapToResponse(job);
    }

    private OcrJobResponse mapToResponse(OcrJob job) {

        OcrJobResponse response = new OcrJobResponse();

        response.setId(job.getId());
        response.setDocumentId(job.getDocument().getId());
        response.setDocumentTitle(job.getDocument().getTitle());
        response.setEngine(job.getEngine());
        response.setStatus(job.getStatus());
        response.setExtractedText(job.getExtractedText());
        response.setCreatedAt(job.getCreatedAt());
        response.setStartedAt(job.getStartedAt());
        response.setCompletedAt(job.getCompletedAt());

        return response;
    }
}