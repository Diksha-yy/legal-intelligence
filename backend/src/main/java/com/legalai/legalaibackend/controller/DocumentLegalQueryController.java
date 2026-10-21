package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.DocumentLegalQueryRequest;
import com.legalai.legalaibackend.dto.DocumentLegalQueryResponse;
import com.legalai.legalaibackend.service.DocumentLegalQueryService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/legal-query")
@RequiredArgsConstructor
public class DocumentLegalQueryController {

    private final DocumentLegalQueryService documentLegalQueryService;

    /**
     * Ask a question about an uploaded document.
     */
    @PostMapping("/ask")
    public ResponseEntity<DocumentLegalQueryResponse> askQuestion(
            @Valid @RequestBody DocumentLegalQueryRequest request) {

        DocumentLegalQueryResponse response =
                documentLegalQueryService.askQuestion(request);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(response);
    }

    /**
     * Get all questions asked for a document.
     */
    @GetMapping("/history/{documentId}")
    public ResponseEntity<List<DocumentLegalQueryResponse>> getHistory(
            @PathVariable Long documentId) {

        return ResponseEntity.ok(
                documentLegalQueryService.getQuestionHistory(documentId)
        );
    }

    /**
     * Get one Q&A by ID.
     */
    @GetMapping("/{queryId}")
    public ResponseEntity<DocumentLegalQueryResponse> getQuestion(
            @PathVariable Long queryId) {

        return ResponseEntity.ok(
                documentLegalQueryService.getQuestionById(queryId)
        );
    }

    /**
     * Delete one Q&A.
     */
    @DeleteMapping("/{queryId}")
    public ResponseEntity<String> deleteQuestion(
            @PathVariable Long queryId) {

        documentLegalQueryService.deleteQuestion(queryId);

        return ResponseEntity.ok(
                "Question deleted successfully."
        );
    }

    /**
     * Delete all Q&A history for a document.
     */
    @DeleteMapping("/history/{documentId}")
    public ResponseEntity<String> deleteHistory(
            @PathVariable Long documentId) {

        documentLegalQueryService.deleteDocumentHistory(documentId);

        return ResponseEntity.ok(
                "Document question history deleted successfully."
        );
    }
}