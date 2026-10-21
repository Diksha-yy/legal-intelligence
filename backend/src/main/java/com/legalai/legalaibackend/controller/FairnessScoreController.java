package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.FairnessScoreRequest;
import com.legalai.legalaibackend.dto.FairnessScoreResponse;
import com.legalai.legalaibackend.service.FairnessScoreService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/fairness")
public class FairnessScoreController {

    private final FairnessScoreService fairnessScoreService;

    public FairnessScoreController(FairnessScoreService fairnessScoreService) {
        this.fairnessScoreService = fairnessScoreService;
    }

    // Create or Update Fairness Score
    @PostMapping
    public ResponseEntity<FairnessScoreResponse> saveFairnessScore(
            @Valid @RequestBody FairnessScoreRequest request) {

        FairnessScoreResponse response =
                fairnessScoreService.saveFairnessScore(request);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(response);
    }

    // Get by Document ID
    @GetMapping("/document/{documentId}")
    public ResponseEntity<FairnessScoreResponse> getByDocumentId(
            @PathVariable Long documentId) {

        return ResponseEntity.ok(
                fairnessScoreService.getByDocumentId(documentId)
        );
    }

    // Get All
    @GetMapping
    public ResponseEntity<List<FairnessScoreResponse>> getAll() {

        return ResponseEntity.ok(
                fairnessScoreService.getAll()
        );
    }

    // Delete by Document ID
    @DeleteMapping("/document/{documentId}")
    public ResponseEntity<String> delete(
            @PathVariable Long documentId) {

        fairnessScoreService.delete(documentId);

        return ResponseEntity.ok(
                "Fairness Score deleted successfully."
        );
    }
}