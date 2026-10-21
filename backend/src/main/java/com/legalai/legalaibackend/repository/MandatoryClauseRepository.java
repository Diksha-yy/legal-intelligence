package com.legalai.legalaibackend.repository;

import com.legalai.legalaibackend.entity.DocumentType;
import com.legalai.legalaibackend.entity.MandatoryClause;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface MandatoryClauseRepository extends JpaRepository<MandatoryClause, Long> {

    List<MandatoryClause> findByDocumentType(DocumentType documentType);

    List<MandatoryClause> findByDocumentTypeId(Long documentTypeId);

}