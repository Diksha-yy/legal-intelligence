package com.legalai.legalaibackend.mapper;

import com.legalai.legalaibackend.dto.FairnessScoreRequest;
import com.legalai.legalaibackend.dto.FairnessScoreResponse;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.FairnessScore;
import org.springframework.stereotype.Component;

@Component
public class FairnessScoreMapper {

    // Request DTO -> Entity
    public FairnessScore toEntity(
            FairnessScoreRequest request,
            Document document) {

        FairnessScore fairnessScore = new FairnessScore();

        fairnessScore.setDocument(document);
        fairnessScore.setFairnessScore(request.getFairnessScore());
        fairnessScore.setRightsPartyA(request.getRightsPartyA());
        fairnessScore.setRightsPartyB(request.getRightsPartyB());
        fairnessScore.setObligationsPartyA(request.getObligationsPartyA());
        fairnessScore.setObligationsPartyB(request.getObligationsPartyB());
        fairnessScore.setPenaltiesPartyA(request.getPenaltiesPartyA());
        fairnessScore.setPenaltiesPartyB(request.getPenaltiesPartyB());
        fairnessScore.setExplanation(request.getExplanation());

        return fairnessScore;
    }

    // Entity -> Response DTO
    public FairnessScoreResponse toResponse(FairnessScore fairnessScore) {

        FairnessScoreResponse response = new FairnessScoreResponse();

        response.setId(fairnessScore.getId());
        response.setDocumentId(fairnessScore.getDocument().getId());

        response.setFairnessScore(fairnessScore.getFairnessScore());

        response.setRightsPartyA(fairnessScore.getRightsPartyA());
        response.setRightsPartyB(fairnessScore.getRightsPartyB());

        response.setObligationsPartyA(fairnessScore.getObligationsPartyA());
        response.setObligationsPartyB(fairnessScore.getObligationsPartyB());

        response.setPenaltiesPartyA(fairnessScore.getPenaltiesPartyA());
        response.setPenaltiesPartyB(fairnessScore.getPenaltiesPartyB());

        response.setExplanation(fairnessScore.getExplanation());

        response.setCreatedAt(fairnessScore.getCreatedAt());
        response.setUpdatedAt(fairnessScore.getUpdatedAt());

        return response;
    }
}