package com.legalai.legalaibackend.service.impl;

import com.legalai.legalaibackend.dto.FairnessScoreRequest;
import com.legalai.legalaibackend.dto.FairnessScoreResponse;
import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.FairnessScore;
import com.legalai.legalaibackend.exception.ResourceNotFoundException;
import com.legalai.legalaibackend.mapper.FairnessScoreMapper;
import com.legalai.legalaibackend.repository.DocumentRepository;
import com.legalai.legalaibackend.repository.FairnessScoreRepository;
import com.legalai.legalaibackend.service.FairnessScoreService;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
@Transactional
public class FairnessScoreServiceImpl implements FairnessScoreService {

    private final FairnessScoreRepository fairnessScoreRepository;
    private final DocumentRepository documentRepository;
    private final FairnessScoreMapper fairnessScoreMapper;

    public FairnessScoreServiceImpl(
            FairnessScoreRepository fairnessScoreRepository,
            DocumentRepository documentRepository,
            FairnessScoreMapper fairnessScoreMapper) {

        this.fairnessScoreRepository = fairnessScoreRepository;
        this.documentRepository = documentRepository;
        this.fairnessScoreMapper = fairnessScoreMapper;
    }

    @Override
    public FairnessScoreResponse saveFairnessScore(FairnessScoreRequest request) {

        Document document = documentRepository.findById(request.getDocumentId())
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Document not found with id: " + request.getDocumentId()));

        FairnessScore fairnessScore = fairnessScoreRepository
                .findByDocumentId(request.getDocumentId())
                .orElseGet(() ->
                        fairnessScoreMapper.toEntity(request, document));

        // Update existing values
        fairnessScore.setDocument(document);
        fairnessScore.setFairnessScore(request.getFairnessScore());
        fairnessScore.setRightsPartyA(request.getRightsPartyA());
        fairnessScore.setRightsPartyB(request.getRightsPartyB());
        fairnessScore.setObligationsPartyA(request.getObligationsPartyA());
        fairnessScore.setObligationsPartyB(request.getObligationsPartyB());
        fairnessScore.setPenaltiesPartyA(request.getPenaltiesPartyA());
        fairnessScore.setPenaltiesPartyB(request.getPenaltiesPartyB());
        fairnessScore.setExplanation(request.getExplanation());

        FairnessScore saved = fairnessScoreRepository.save(fairnessScore);

        return fairnessScoreMapper.toResponse(saved);
    }

    @Override
    public FairnessScoreResponse getByDocumentId(Long documentId) {

        FairnessScore fairnessScore = fairnessScoreRepository
                .findByDocumentId(documentId)
                .orElseThrow(() ->
                        new ResourceNotFoundException(
                                "Fairness Score not found for document id: " + documentId));

        return fairnessScoreMapper.toResponse(fairnessScore);
    }

    @Override
    public List<FairnessScoreResponse> getAll() {

        return fairnessScoreRepository.findAll()
                .stream()
                .map(fairnessScoreMapper::toResponse)
                .collect(Collectors.toList());
    }

    @Override
    public void delete(Long documentId) {

        if (!fairnessScoreRepository.existsByDocumentId(documentId)) {
            throw new ResourceNotFoundException(
                    "Fairness Score not found for document id: " + documentId);
        }

        fairnessScoreRepository.deleteByDocumentId(documentId);
    }
}