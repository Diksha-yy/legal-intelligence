package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.DocumentSummaryResponse;
import com.legalai.legalaibackend.service.DocumentSummaryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/summary")
public class DocumentSummaryController {

    private final DocumentSummaryService documentSummaryService;

    public DocumentSummaryController(DocumentSummaryService documentSummaryService) {
        this.documentSummaryService = documentSummaryService;
    }

    @PostMapping("/generate/{documentId}")
    public ResponseEntity<DocumentSummaryResponse> generateSummary(
            @PathVariable Long documentId) {

        DocumentSummaryResponse response =
                documentSummaryService.generateSummary(documentId);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/{documentId}")
    public ResponseEntity<DocumentSummaryResponse> getSummary(
            @PathVariable Long documentId) {

        DocumentSummaryResponse response =
                documentSummaryService.getSummary(documentId);

        return ResponseEntity.ok(response);
    }
}