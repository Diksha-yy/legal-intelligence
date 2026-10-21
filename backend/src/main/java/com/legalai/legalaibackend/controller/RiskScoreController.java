package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.RiskScoreResponse;
import com.legalai.legalaibackend.service.RiskScoreService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/risk-score")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class RiskScoreController {

    private final RiskScoreService riskScoreService;

    @GetMapping("/{documentId}")
    public ResponseEntity<RiskScoreResponse> calculateRiskScore(
            @PathVariable Long documentId) {

        RiskScoreResponse response =
                riskScoreService.calculateRiskScore(documentId);

        return ResponseEntity.ok(response);
    }
}