package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.AgreementComparisonRequest;
import com.legalai.legalaibackend.dto.AgreementComparisonResponse;
import com.legalai.legalaibackend.service.AgreementComparisonService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/agreement-comparison")
@RequiredArgsConstructor
public class AgreementComparisonController {

    private final AgreementComparisonService agreementComparisonService;

    @PostMapping
    public ResponseEntity<AgreementComparisonResponse> compareAgreements(
            @Valid @RequestBody AgreementComparisonRequest request) {

        AgreementComparisonResponse response =
                agreementComparisonService.compareAgreements(request);

        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/{comparisonId}")
    public ResponseEntity<AgreementComparisonResponse> getComparisonById(
            @PathVariable Long comparisonId) {

        return ResponseEntity.ok(
                agreementComparisonService.getComparisonById(comparisonId)
        );
    }

    @GetMapping("/history/{documentId}")
    public ResponseEntity<List<AgreementComparisonResponse>> getComparisonHistory(
            @PathVariable Long documentId) {

        return ResponseEntity.ok(
                agreementComparisonService.getComparisonHistory(documentId)
        );
    }

    @DeleteMapping("/{comparisonId}")
    public ResponseEntity<String> deleteComparison(
            @PathVariable Long comparisonId) {

        agreementComparisonService.deleteComparison(comparisonId);

        return ResponseEntity.ok("Agreement comparison deleted successfully.");
    }
}