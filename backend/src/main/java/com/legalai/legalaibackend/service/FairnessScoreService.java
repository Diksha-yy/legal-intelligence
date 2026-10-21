package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.FairnessScoreRequest;
import com.legalai.legalaibackend.dto.FairnessScoreResponse;

import java.util.List;

public interface FairnessScoreService {

    FairnessScoreResponse saveFairnessScore(FairnessScoreRequest request);

    FairnessScoreResponse getByDocumentId(Long documentId);

    List<FairnessScoreResponse> getAll();

    void delete(Long documentId);
}