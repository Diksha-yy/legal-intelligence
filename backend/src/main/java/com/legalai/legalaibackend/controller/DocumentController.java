package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.DocumentRequest;
import com.legalai.legalaibackend.dto.DocumentResponse;
import com.legalai.legalaibackend.service.DocumentService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/api/documents")
public class DocumentController {

    @Autowired
    private DocumentService documentService;

    // =====================================
    // Save Document (JSON)
    // =====================================
    @PostMapping
    public ResponseEntity<DocumentResponse> saveDocument(
            @Valid @RequestBody DocumentRequest request) {

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(documentService.saveDocument(request));
    }

    // =====================================
    // Upload Document
    // =====================================
    @PostMapping(
            value = "/upload",
            consumes = MediaType.MULTIPART_FORM_DATA_VALUE
    )
    public ResponseEntity<DocumentResponse> uploadDocument(
            @RequestPart("file") MultipartFile file,
            @RequestParam("title") String title,
            @RequestParam("userId") Long userId) {

        return ResponseEntity.status(HttpStatus.CREATED)
                .body(documentService.uploadDocument(file, title, userId));
    }

    // =====================================
    // Get All Documents
    // =====================================
    @GetMapping
    public ResponseEntity<List<DocumentResponse>> getAllDocuments() {

        return ResponseEntity.ok(documentService.getAllDocuments());
    }

    // =====================================
    // Get By ID
    // =====================================
    @GetMapping("/{id}")
    public ResponseEntity<DocumentResponse> getDocumentById(
            @PathVariable Long id) {

        return ResponseEntity.ok(documentService.getDocumentById(id));
    }

    // =====================================
    // Delete
    // =====================================
    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteDocument(
            @PathVariable Long id) {

        documentService.deleteDocument(id);

        return ResponseEntity.ok("Document deleted successfully.");
    }
}