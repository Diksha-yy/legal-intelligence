package com.legalai.legalaibackend.repository;

import com.legalai.legalaibackend.entity.AgreementComparison;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AgreementComparisonRepository extends JpaRepository<AgreementComparison, Long> {

    List<AgreementComparison> findByVersionADocumentId(Long documentId);

    List<AgreementComparison> findByVersionBDocumentId(Long documentId);

    List<AgreementComparison> findByVersionADocumentIdOrVersionBDocumentId(
            Long versionADocumentId,
            Long versionBDocumentId
    );

}