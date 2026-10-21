package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.MissingClauseResponse;

public interface MissingClauseService {

    MissingClauseResponse detectMissingClauses(
            Long documentId,
            Long documentTypeId
    );

}