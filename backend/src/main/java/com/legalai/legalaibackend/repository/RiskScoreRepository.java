package com.legalai.legalaibackend.repository;

import com.legalai.legalaibackend.entity.RiskScore;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface RiskScoreRepository extends JpaRepository<RiskScore, Long> {

    Optional<RiskScore> findByDocumentId(Long documentId);

    boolean existsByDocumentId(Long documentId);

}