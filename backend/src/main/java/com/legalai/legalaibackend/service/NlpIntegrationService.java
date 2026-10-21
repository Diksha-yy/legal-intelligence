package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.MissingClauseResponse;

public interface NlpIntegrationService {

    MissingClauseResponse analyzeDocument(Long documentId, Long documentTypeId);

}