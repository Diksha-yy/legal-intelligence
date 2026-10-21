package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.OcrJobResponse;
import com.legalai.legalaibackend.service.OcrJobService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/ocr")
public class OcrJobController {

    private final OcrJobService ocrJobService;

    public OcrJobController(OcrJobService ocrJobService) {
        this.ocrJobService = ocrJobService;
    }

    @PostMapping("/start/{documentId}")
    public ResponseEntity<OcrJobResponse> startOcr(
            @PathVariable Long documentId) {

        OcrJobResponse response = ocrJobService.startOcr(documentId);
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{documentId}")
    public ResponseEntity<OcrJobResponse> getLatestJob(
            @PathVariable Long documentId) {

        OcrJobResponse response = ocrJobService.getLatestJob(documentId);
        return ResponseEntity.ok(response);
    }
}