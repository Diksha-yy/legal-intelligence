package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.DocumentAnalysisRequest;
import com.legalai.legalaibackend.dto.DocumentAnalysisResponse;
import com.legalai.legalaibackend.service.DocumentAnalysisService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/document-analysis")
@CrossOrigin(origins = "*")
public class DocumentAnalysisController {

    private final DocumentAnalysisService documentAnalysisService;

    public DocumentAnalysisController(DocumentAnalysisService documentAnalysisService) {
        this.documentAnalysisService = documentAnalysisService;
    }

    @PostMapping("/analyze")
    public DocumentAnalysisResponse analyzeDocument(
            @Valid @RequestBody DocumentAnalysisRequest request) {

        return documentAnalysisService.analyzeDocument(
                request.getDocumentType(),
                request.getDetectedClauses()
        );
    }
}