package com.legalai.legalaibackend.service;

import com.legalai.legalaibackend.dto.OcrJobResponse;

public interface OcrJobService {

    /**
     * Starts OCR processing for the given document.
     *
     * @param documentId document id
     * @return OCR job response
     */
    OcrJobResponse startOcr(Long documentId);

    /**
     * Returns the latest OCR job for the given document.
     *
     * @param documentId document id
     * @return OCR job response
     */
    OcrJobResponse getLatestJob(Long documentId);
}