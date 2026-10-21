package com.legalai.legalaibackend.controller;

import com.legalai.legalaibackend.dto.MissingClauseResponse;
import com.legalai.legalaibackend.service.MissingClauseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/missing-clauses")
@CrossOrigin(origins = "*")
public class MissingClauseController {

    @Autowired
    private MissingClauseService missingClauseService;

    @GetMapping("/check")
    public MissingClauseResponse detectMissingClauses(
            @RequestParam Long documentId,
            @RequestParam Long documentTypeId
    ) {

        return missingClauseService.detectMissingClauses(
                documentId,
                documentTypeId
        );
    }
}