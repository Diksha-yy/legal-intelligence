package com.legalai.legalaibackend.integration;

import com.legalai.legalaibackend.dto.AiLegalQueryRequest;
import com.legalai.legalaibackend.dto.AiLegalQueryResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
@RequiredArgsConstructor
public class AiServiceClientImpl implements AiServiceClient {

    private final RestTemplate restTemplate;

    @Value("${ai.service.base-url}")
    private String aiServiceBaseUrl;

    @Override
    public AiLegalQueryResponse askQuestion(AiLegalQueryRequest request) {

        String url = aiServiceBaseUrl + "/api/rag/ask";

        HttpEntity<AiLegalQueryRequest> httpEntity =
                new HttpEntity<>(request);

        ResponseEntity<AiLegalQueryResponse> response =
                restTemplate.exchange(
                        url,
                        HttpMethod.POST,
                        httpEntity,
                        AiLegalQueryResponse.class
                );

        return response.getBody();
    }
}