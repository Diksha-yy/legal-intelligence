package com.legalai.legalaibackend.repository;

import com.legalai.legalaibackend.entity.DocumentLegalQuery;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DocumentLegalQueryRepository
        extends JpaRepository<DocumentLegalQuery, Long> {

    /**
     * Get all questions asked for a document.
     */
    List<DocumentLegalQuery> findByDocumentId(Long documentId);

    /**
     * Get latest questions first.
     */
    List<DocumentLegalQuery> findByDocumentIdOrderByCreatedAtDesc(Long documentId);

    /**
     * Search question text.
     */
    List<DocumentLegalQuery> findByQuestionContainingIgnoreCase(String keyword);

    /**
     * Search answer text.
     */
    List<DocumentLegalQuery> findByAnswerContainingIgnoreCase(String keyword);

    /**
     * Delete all Q&A history of a document.
     */
    void deleteByDocumentId(Long documentId);

    /**
     * Check whether a document has any Q&A history.
     */
    boolean existsByDocumentId(Long documentId);

    /**
     * Count total questions asked for a document.
     */
    long countByDocumentId(Long documentId);
}