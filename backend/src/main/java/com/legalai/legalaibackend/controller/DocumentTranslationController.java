package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.DocumentTranslationResponse;
import com.legalai.legalaibackend.service.DocumentTranslationService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/translation")
public class DocumentTranslationController {

    private final DocumentTranslationService translationService;

    public DocumentTranslationController(DocumentTranslationService translationService) {
        this.translationService = translationService;
    }

    @PostMapping("/generate/{documentId}")
    public ResponseEntity<DocumentTranslationResponse> generateTranslation(
            @PathVariable Long documentId,
            @RequestParam String language) {

        DocumentTranslationResponse response =
                translationService.generateTranslation(documentId, language);

        return ResponseEntity.ok(response);
    }

    @GetMapping("/{documentId}")
    public ResponseEntity<DocumentTranslationResponse> getTranslation(
            @PathVariable Long documentId) {

        DocumentTranslationResponse response =
                translationService.getTranslation(documentId);

        return ResponseEntity.ok(response);
    }
}