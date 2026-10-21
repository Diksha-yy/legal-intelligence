package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.MissingClauseResponse;
import com.legalai.legalaibackend.service.NlpIntegrationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/nlp")
@CrossOrigin(origins = "*")
public class NlpIntegrationController {

    @Autowired
    private NlpIntegrationService nlpIntegrationService;

    @PostMapping("/analyze")
    public MissingClauseResponse analyzeDocument(
            @RequestParam Long documentId,
            @RequestParam Long documentTypeId) {

        return nlpIntegrationService.analyzeDocument(
                documentId,
                documentTypeId
        );
    }
}