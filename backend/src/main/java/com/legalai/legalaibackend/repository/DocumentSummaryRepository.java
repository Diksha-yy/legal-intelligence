package com.legalai.legalaibackend.repository;

import com.legalai.legalaibackend.entity.Document;
import com.legalai.legalaibackend.entity.DocumentSummary;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface DocumentSummaryRepository extends JpaRepository<DocumentSummary, Long> {

    /**
     * Returns the summary for a document if it exists.
     */
    Optional<DocumentSummary> findByDocument(Document document);

    /**
     * Check whether a summary already exists.
     */
    boolean existsByDocument(Document document);

    /**
     * Delete summary when document is deleted (optional but useful).
     */
    void deleteByDocument(Document document);
}