package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.AgreementComparisonRequest;
import com.legalai.legalaibackend.dto.AgreementComparisonResponse;

import java.util.List;

public interface AgreementComparisonService {

    AgreementComparisonResponse compareAgreements(
            AgreementComparisonRequest request
    );

    AgreementComparisonResponse getComparisonById(Long comparisonId);

    List<AgreementComparisonResponse> getComparisonHistory(Long documentId);

    void deleteComparison(Long comparisonId);

}