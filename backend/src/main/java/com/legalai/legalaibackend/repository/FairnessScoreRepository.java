package com.legalai.legalaibackend.repository;

import com.legalai.legalaibackend.entity.FairnessScore;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface FairnessScoreRepository extends JpaRepository<FairnessScore, Long> {

    Optional<FairnessScore> findByDocumentId(Long documentId);

    boolean existsByDocumentId(Long documentId);

    void deleteByDocumentId(Long documentId);
}