package com.legalai.legalaibackend.integration;

import com.legalai.legalaibackend.dto.AiLegalQueryRequest;
import com.legalai.legalaibackend.dto.AiLegalQueryResponse;

public interface AiServiceClient {

    /**
     * Sends a legal question to the AI service
     * and returns the generated answer.
     *
     * @param request AI query request
     * @return AI-generated response
     */
    AiLegalQueryResponse askQuestion(AiLegalQueryRequest request);

}