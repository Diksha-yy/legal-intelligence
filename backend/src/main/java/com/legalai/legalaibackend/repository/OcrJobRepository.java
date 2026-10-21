package com.legalai.legalaibackend.repository;

import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.OcrJob;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface OcrJobRepository extends JpaRepository<OcrJob, Long> {

    Optional<OcrJob> findTopByDocumentOrderByCreatedAtDesc(Document document);

    Optional<OcrJob> findByDocument(Document document);

    boolean existsByDocument(Document document);
}